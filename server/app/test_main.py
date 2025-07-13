from fastapi.testclient import TestClient
from firebase_admin.auth import UserRecord, UserNotFoundError
from httpx import request
from .config.settings import settings
from .main import app
from firebase_admin import auth
from faker import Faker

client = TestClient(app)

TEST_FIREBASE_USER = {
    "email": "test@gmail.com",
    "full_name": "Nicholas",
    "password": "test2342",
}

faker = Faker()


def _ensure_test_user(**kwargs: dict | None) -> UserRecord:
    try:
        payload = kwargs.get("email") or TEST_FIREBASE_USER.get("email")
        return auth.get_user_by_email(payload)
    except UserNotFoundError:
        payload = kwargs or TEST_FIREBASE_USER
        if "full_name" in payload:
            payload["display_name"] = payload.pop("full_name")
        return auth.create_user(**payload)


def get_id_token(**kwargs: dict | None) -> str:
    user = _ensure_test_user(**kwargs)
    custom_token = auth.create_custom_token(user.uid).decode()

    url = (
        "https://identitytoolkit.googleapis.com/v1/"
        f"accounts:signInWithCustomToken?key={settings.FIREBASE_WEB_API_KEY}"
    )
    res = request(
        method="post",
        url=url,
        json={"token": custom_token, "returnSecureToken": True},
        timeout=5,
    )
    res.raise_for_status()
    return res.json()["idToken"]


def test_current_user_me() -> None:
    token = get_id_token()
    response = client.get(
        f"{settings.api_base_path}/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    record = response.json()
    assert response.status_code == 200
    assert record.get("email") == TEST_FIREBASE_USER.get("email")
    assert record.get("full_name") == TEST_FIREBASE_USER.get("full_name")


def test_create_user() -> None:
    current_user_data = {
        "email": faker.email(),
        "full_name": faker.name(),
        "password": faker.password(),
    }
    token = get_id_token(**current_user_data)

    response = client.post(
        f"{settings.api_base_path}/users",
        headers={"Authorization": f"Bearer {token}"},
        json=current_user_data,
    )

    record = response.json()
    assert response.status_code == 201
    assert record.get("email") == current_user_data.get("email")
    assert record.get("full_name") == current_user_data.get("full_name")
