from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth


from src.sub_apps.auth_app.routers.auth_router import AuthRouter

starlette_config = Config("oauth_with_fastapi_variables.env")
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
    },
)

routers = [AuthRouter(oauth)]

auth_app = FastAPI()
auth_app.add_middleware(SessionMiddleware, secret_key="c")


for router in routers:
    auth_app.include_router(router.router)
