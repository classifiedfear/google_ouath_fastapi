from fastapi import FastAPI
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth


from src.sub_apps.auth_app.router_controllers.auth_router_controller import AuthRouterController

starlette_config = Config("src/oauth_with_fastapi_variables.env")
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
    },
)

routers = [AuthRouterController(oauth)]

auth_app = FastAPI()

for router in routers:
    auth_app.include_router(router.router)
