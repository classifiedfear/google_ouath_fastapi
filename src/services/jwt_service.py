from datetime import datetime, timedelta, timezone

from typing import Any, Dict
import jwt

from src.settings import Settings


class JWTService:
    def __init__(self, settings: Settings):
        self._settings = settings

    def create_access_token(self, data: Dict[str, Any], expires_delta: int = 15) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self._settings.API_SECRET_KEY, algorithm=self._settings.API_ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str) -> Dict[str, Any]:
        return jwt.decode(
            token, self._settings.API_SECRET_KEY, algorithms=[self._settings.API_ALGORITHM]
        )

    def create_refresh_token(
        self,
        data: Dict[str, Any],
    ) -> str:
        return self.create_access_token(
            data,
            expires_delta=self._settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )
