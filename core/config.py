from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5434/postgres"
    db_echo: bool = True


settings = Setting()
