from datetime import datetime, UTC
from typing import Any, Dict
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth

from src.services.email_validator_service import valid_email_from_db
from src.sub_apps.auth_app.exceptions import CREDENTIALS_EXCEPTION
from src.dependencies.services import JWT_SERVICE
from src.fake_db.db import add_blacklist_token, add_user_info, remove_user_info


class AuthRouter:
    def __init__(self, oauth: OAuth) -> None:
        self._router = APIRouter()
        self._oauth = oauth
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route("/", self._test, methods=["GET"])
        self._router.add_api_route("/login_google/", self._login_google, methods=["GET"])
        self._router.add_api_route("/auth_google", self._auth_google, methods=["GET"])
        self._router.add_api_route("/logout", self._logout, methods=["GET"])
        #self._router.add_api_route("/refresh", self._refresh_token, methods=["GET"])

    def _test(self) -> JSONResponse:
        return JSONResponse({"message": "auth_app"})

    async def _login_google(self, request: Request):
        redirect_uri = "http://127.0.0.1:7000/token"
        return await self._oauth.google.authorize_redirect(request, redirect_uri)

    async def _logout(self):
        remove_user_info()
        return RedirectResponse("/")


    async def _auth_google(self, request: Request, jwt_service: JWT_SERVICE):
        access_token: Dict[str, Any] = await self._oauth.google.authorize_access_token(request)
        user_info: Dict[str, Any] = access_token.get("userinfo")
        add_user_info(user_info)
        return JSONResponse(
            {
                "result": True,
                "access_token": jwt_service.create_access_token(
                    {"sub": user_info["email"]}, expires_delta=15
                ),
                "refresh_token": jwt_service.create_refresh_token({"sub": user_info["email"]}),
            }
        )

    #async def _refresh_token(
    #    self,
    #    request: Request,
    #    jwt_service: JWT_SERVICE,
    #):
    #    try:
    #        if request.method == "POST":
    #            form = await request.json()
    #            if form.get("grant_type") == "refresh_token":
    #                token = form.get("refresh_token")
    #                payload = jwt_service.decode_token(token)
    #                if datetime.fromtimestamp(payload.get("exp"), tz=UTC) > datetime.now(UTC):
    #                    email = payload.get("sub")
    #                    if valid_email_from_db(email):
    #                        return JSONResponse(
    #                            {
    #                                "result": True,
    #                                "access_token": jwt_service.create_access_token({"sub": email}),
    #                            }
    #                        )
#
    #    except Exception:
    #        raise CREDENTIALS_EXCEPTION
    #    raise CREDENTIALS_EXCEPTION
