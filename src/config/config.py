from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    environment: str = "development"
    port: int = 8000

    database_url: str
    database_name: str

    secret: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float
    MAX_FILE_SIZE: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


config = Config()
