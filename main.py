from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sub_apps.auth_app.auth import auth_app
from sub_apps.api_app.api import api_app
from routers.main_router import MainRouter
from fake_db.db import init_blacklist_file
#from middlewares.error_handling_middleware import ErrorHandlingMiddleware


init_blacklist_file()
app = FastAPI()

app.mount("/auth", auth_app)
app.mount("/api", api_app)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
routers = [MainRouter(templates)]
#app.add_middleware(ErrorHandlingMiddleware)


for router in routers:
    app.include_router(router.router)
