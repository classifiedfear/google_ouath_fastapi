from fastapi import Request
from fastapi.templating import Jinja2Templates

from src.router_controllers.abstract_router_controller import AbstractRouterController


class MainRouterController(AbstractRouterController):
    def __init__(self, templates: Jinja2Templates) -> None:
        self._templates = templates
        self._init_routes()

    def _init_routes(self) -> None:
        self._router.add_api_route("/", self._homepage, methods=["GET"])
        self._router.add_api_route("/token", self._google_info, methods=["GET"])
        self._router.add_api_route("/google_info", self._google_info, methods=["GET"])

    async def _homepage(self, request: Request):
        user = request.session.get("user")
        if user:
            return self._templates.TemplateResponse(
                name="welcome.html", context={"request": request, "user_info": user}
            )
        return self._templates.TemplateResponse(name="home.html", context={"request": request})

    async def _google_info(self, request: Request):
        return self._templates.TemplateResponse(
            name="google_info.html",
            context={"request": request, "user_info": request.session.get("user")},
        )
