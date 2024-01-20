from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5434/postgres"
    db_echo: bool = True


settings = Setting()
