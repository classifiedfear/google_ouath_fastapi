from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.fake_db.db import get_last_user_info


class MainRouter:
    def __init__(self, templates: Jinja2Templates) -> None:
        self._router = APIRouter()
        self._templates = templates
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route("/", self._homepage, methods=["GET"])
        self._router.add_api_route("/token", self._token, methods=["GET"])

    async def _homepage(self, request: Request):
        user_info = get_last_user_info()
        if user_info:
            html = f"<pre>{user_info}</pre>"
            html += """<a href="/token">Token</a>"""
            return self._templates.TemplateResponse(
                name="welcome.html", context={"request": request, "user_info": user_info}
            )
        return self._templates.TemplateResponse(name="home.html", context={"request": request})

    async def _token(self, request: Request):
        return self._templates.TemplateResponse(name="token.html", context={"request": request})
