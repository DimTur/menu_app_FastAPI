from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

    echo: bool = False


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()


settings = Settings()
