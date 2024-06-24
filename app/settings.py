import os
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


class Settings(BaseSettings):
    debug: bool = False
    secret_key: SecretStr
    environment: str
    https_only: bool

    # database credential
    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    model_config = SettingsConfigDict(env_file=os.path.join(ROOT_DIR, "env", ".env"), extra='ignore')


@lru_cache
def get_settings():
    return Settings()
