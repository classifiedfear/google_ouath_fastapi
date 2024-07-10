from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


from src.services.jwt_service import JWTService
from src.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


SETTINGS = Annotated[Settings, Depends(get_settings)]

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/auth_google")

OAUTH2 = Annotated[str, Depends(oauth2)]


def get_jwt_service(settings: SETTINGS) -> JWTService:
    return JWTService(settings)



JWT_SERVICE = Annotated[JWTService, Depends(get_jwt_service)]
