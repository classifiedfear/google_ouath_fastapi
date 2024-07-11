from abc import ABC, abstractmethod
from fastapi import APIRouter


class AbstractRouterController(ABC):
    _router = APIRouter()

    @property
    def router(self) -> APIRouter:
        return self._router

    @abstractmethod
    def _init_routes(self) -> None:
        pass
