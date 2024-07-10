from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SECRET_KEY: str
    FRONTEND_URL: str
    API_SECRET_KEY: str
    API_ALGORITHM: str
    API_ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
