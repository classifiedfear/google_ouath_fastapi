from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.router_controllers.abstract_router_controller import AbstractRouterController

from src.sub_apps.auth_app.auth import auth_app
from src.settings import SETTINGS


class AppInitializer:
    def __init__(self):
        self._app = FastAPI()
        self._init_middlewares()
        self._mount_apps()

    def _init_middlewares(self) -> None:
        self._app.add_middleware(SessionMiddleware, secret_key=SETTINGS.SECRET_KEY)
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _mount_apps(self) -> None:
        self._app.mount("/src/static", StaticFiles(directory="src/static"), name="static")
        self._app.mount("/auth", auth_app)

    def add_controller(self, controller: AbstractRouterController) -> None:
        self._app.include_router(controller.router)

    @property
    def app(self) -> FastAPI:
        return self._app
