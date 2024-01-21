from pydantic_settings import BaseSettings
from pydantic import BaseModel


class DbSettings(BaseModel):
    url: str = "postgresql+asyncpg://postgres:postgres@localhost:5434/postgres"
    echo: bool = False


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()


settings = Settings()
