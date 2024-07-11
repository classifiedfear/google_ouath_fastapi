from typing import Any, Dict
from fastapi import Request
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

from src.router_controllers.abstract_router_controller import AbstractRouterController
from src.dependencies.services import SETTINGS


class AuthRouterController(AbstractRouterController):
    def __init__(self, oauth: OAuth) -> None:
        self._oauth = oauth
        self._init_routes()

    def _init_routes(self) -> None:
        self._router.add_api_route("/login_google/", self._login_google, methods=["GET"])
        self._router.add_api_route("/auth_google", self._auth_google, methods=["GET"])
        self._router.add_api_route("/logout", self._logout, methods=["GET"])

    async def _login_google(self, request: Request, settings: SETTINGS):
        return await self._oauth.google.authorize_redirect(request, settings.FRONTEND_URL)

    async def _logout(self, request: Request):
        request.session.pop("user", None)
        return RedirectResponse("/")

    async def _auth_google(self, request: Request):
        access_token: Dict[str, Any] = await self._oauth.google.authorize_access_token(request)
        user: Dict[str, Any] = access_token.get("userinfo")
        if user:
            request.session["user"] = user
        return RedirectResponse("/")
