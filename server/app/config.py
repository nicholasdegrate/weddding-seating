from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env"
    )
    # model_config = SettingsConfigDict(
    #     env_file="../.env",
    #     env_ignore_empty=True,
    #     extra="ignore"
    # )
    
    # API_V1_STR: str = "/api/v1"
    
    # PROJECT_NAME: str
    # POSTGRES_SERVER: str
    # POSTGRES_PORT: int = 5432
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str = ""
    # POSTGRES_DB: str = ""
    # ENVIRONMENT: Literal["local", "staging", "production"] = "local"

settings = Settings()