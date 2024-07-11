from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


SETTINGS = Annotated[Settings, Depends(get_settings)]
