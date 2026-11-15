from pydantic_settings import BaseSettings, SettingsConfigDict
import sys


class Config(BaseSettings):
    environment: str = "development"
    port: int = 8000
    database_url: str = ""
    database_name: str = ""
    secret: str = ""
    model_config = SettingsConfigDict(env_file=".env")


try:
    config = Config()
except Exception as e:  # noqa: BLE001
    print("configuration error", e)
    sys.exit(1)
