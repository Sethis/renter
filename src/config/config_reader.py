

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='src/config/env.env', env_file_encoding='utf-8')

    db_url: str


config = Settings()
