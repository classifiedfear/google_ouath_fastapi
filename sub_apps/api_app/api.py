from fastapi import FastAPI

from sub_apps.api_app.routers.api_router import ApiRouter

routers = [ApiRouter()]

api_app = FastAPI()

for router in routers:
    api_app.include_router(router.router)
