from typing import Awaitable, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from authlib.integrations.base_client.errors import MismatchingStateError
from sub_apps.auth_app.exceptions import CREDENTIALS_EXCEPTION


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except MismatchingStateError as exc:
            raise CREDENTIALS_EXCEPTION from exc
