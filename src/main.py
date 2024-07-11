from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from src.router_controllers.abstract_router_controller import AbstractRouterController
from src.router_controllers.main_router_controller import MainRouterController

from src.sub_apps.auth_app.auth import auth_app


class MainApp:
    def __init__(self):
        self._app = FastAPI()
        self._init_middlewares()
        self._mount_apps()

    def _init_middlewares(self) -> None:
        self._app.add_middleware(
            SessionMiddleware, secret_key="OulLJiqkldb436-X6M11hKvr7wvLyG8TPi5PkLf4"
        )
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


templates = Jinja2Templates(directory="src/templates")
routers = [MainRouterController(templates)]
main_app = MainApp()
for router in routers:
    main_app.add_controller(router)
app = main_app.app

