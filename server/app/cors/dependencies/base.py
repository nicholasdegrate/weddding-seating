from fastapi import HTTPException, status, Depends
from fastapi.concurrency import run_in_threadpool
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, _auth_utils,get_app
import google.auth.exceptions
from pydantic import EmailStr
from sqlmodel import SQLModel, select
from typing import Dict, Any

from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.schemas.schema import User


class FirebaseClaims(SQLModel):
    uid: str
    email: EmailStr | None = None
    email_verified: bool | None = None
    iat: int
    exp: int
    firebase: Dict[str, Any]

    class Config:
        orm_mode = True

async def decode_firebase_token(id_token: str) -> FirebaseClaims:
    try:
        decoded: dict = await run_in_threadpool(
            auth.verify_id_token,
            id_token,
            check_revoked=True,
        )
    except _auth_utils.RevokedIdTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token revoked")
    except _auth_utils.ExpiredIdTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")
    except google.auth.exceptions.TransportError:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Auth service unreachable")
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    return FirebaseClaims(**decoded)

auth_scheme = HTTPBearer(auto_error=False)

async def get_firebase_claims(creds: HTTPAuthorizationCredentials | None = Depends(auth_scheme)) -> FirebaseClaims:
    if creds is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing Authorization header", headers={"WWW-Authenticate": "Bearer"})
    return await decode_firebase_token(creds.credentials)

async def get_current_user(
    claims: FirebaseClaims = Depends(get_firebase_claims),
    session: AsyncSession = Depends(get_session),
) -> User:
    result = await session.exec(select(User).where(User.firebase_uid == claims.uid, User.email == claims.email))
    return result.one_or_none()




