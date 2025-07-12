from firebase_admin import credentials, initialize_app, App, _apps  # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib


class Settings(BaseSettings):
    # general
    PROJECT_NAME: str = "wedding-table"
    API_PREFIX: str = "/api"
    API_DEFAULT_VERSION: str = "v1"

    ENVIRONMENT: str | None = None
    POSTGRES_SERVER: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def api_versions(self) -> dict[str, str]:
        return {
            "v1": f"{self.API_PREFIX}/v1",
        }

    @property
    def api_base_path(self) -> str:
        return self.api_versions.get(
            self.API_DEFAULT_VERSION, f"{self.API_PREFIX}/{self.API_DEFAULT_VERSION}"
        )

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


def init_firebase_admin_app():
    base_dir = pathlib.Path(__file__).resolve().parents[2]
    service_account_path = base_dir / "service-account.json"
    service_account = credentials.Certificate(service_account_path)
    default_app: App | None = None

    if not _apps:
        default_app = initialize_app(
            credential=service_account,
        )

    return default_app

settings = Settings()
