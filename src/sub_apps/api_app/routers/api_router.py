from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse

from src.dependencies.services import OAUTH2, JWT_SERVICE
from src.services.email_validator_service import get_current_user_email
from src.fake_db.db import get_last_user_info


class ApiRouter:
    def __init__(self) -> None:
        self._router = APIRouter()
        self._init_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _init_routes(self) -> None:
        self._router.add_api_route("/unprotected", self._unprotected, methods=["GET"])
        self._router.add_api_route("/protected", self._protected, methods=["GET"])
        self._router.add_api_route("/show_last", self._show_last_user_info, methods=["GET"])

    def _unprotected(self) -> JSONResponse:
        return JSONResponse({"message": "uprotected api_app endpoint"})

    def _protected(self, token: OAUTH2, jwt_service: JWT_SERVICE) -> JSONResponse:
        _ = get_current_user_email(jwt_service.decode_token(token))
        return JSONResponse({"message": "protected api_app endpoint"})

    async def _show_last_user_info(self) -> HTMLResponse:
        user_info = get_last_user_info()
        if user_info:
            html = f"<pre>{user_info}</pre>"
            html += """<button onClick='fetch("http://127.0.0.1:7000/auth/logout",{
        headers:{
            "Authorization": "Bearer " + window.localStorage.getItem("jwt")
        },
    }).then((r)=>r.json()).then((msg)=>{
        console.log(msg);
        if (msg["result"] === true) {
            window.localStorage.removeItem("jwt");
        }
        });'>
    Logout
    </button>"""
            return HTMLResponse(html)
        return HTMLResponse("<pre>No info</pre>")
