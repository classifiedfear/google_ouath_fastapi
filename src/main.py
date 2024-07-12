from fastapi.templating import Jinja2Templates


from src.fastapi_app_initializer.app_initializer import AppInitializer
from src.router_controllers.main_router_controller import MainRouterController


templates = Jinja2Templates(directory="src/templates")
routers = [MainRouterController(templates)]
main_app = AppInitializer()
for router in routers:
    main_app.add_controller(router)
app = main_app.app
