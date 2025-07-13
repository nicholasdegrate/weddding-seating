from fastapi import HTTPException, status, Depends
from fastapi.concurrency import run_in_threadpool
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth
import google.auth.exceptions
from pydantic import EmailStr
from sqlmodel import SQLModel
from typing import Dict, Any, cast
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_session
from app.schemas.schema import User
from sqlmodel.sql.expression import SelectOfScalar


class FirebaseClaims(SQLModel):
    uid: str
    email: EmailStr | None = None
    email_verified: bool | None = None
    iat: int
    exp: int
    firebase: Dict[str, Any]


async def decode_firebase_token(id_token: str) -> FirebaseClaims:
    try:
        decoded: dict = await run_in_threadpool(
            auth.verify_id_token,
            id_token,
            check_revoked=True,
        )
    except google.auth.exceptions.TransportError:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Auth service unreachable"
        )
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, e.__str__())

    return FirebaseClaims(**decoded)


auth_scheme = HTTPBearer(auto_error=False)


async def get_firebase_claims(
    creds: HTTPAuthorizationCredentials | None = Depends(auth_scheme),
) -> FirebaseClaims:
    if creds is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await decode_firebase_token(creds.credentials)


async def get_current_user(
    claims: FirebaseClaims = Depends(get_firebase_claims),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    stmt = (
        select(User)
        .where(User.firebase_uid == claims.uid)
        .where(User.email == claims.email)
    )

    stmt_scalar: SelectOfScalar[User] = cast(SelectOfScalar[User], stmt)
    result = await session.exec(stmt_scalar)
    return result.one_or_none()
