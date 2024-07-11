from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SECRET_KEY: str
    FRONTEND_URL: str
    model_config = SettingsConfigDict(env_file="src/oauth_with_fastapi_variables.env", env_file_encoding="utf-8")
