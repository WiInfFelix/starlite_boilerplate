import uvicorn
from starlite import Starlite, StructLoggingConfig

from src.app.controllers.auth_controller import login_handler, jwt_cookie_auth, register_user
from src.app.controllers.user_controller import UserController
from src.app.database.setup_db import on_startup, sqlalchemy_plugin


logging_config = StructLoggingConfig()

app = Starlite(
    route_handlers=[UserController, login_handler, register_user],
    on_startup=[on_startup],
    on_app_init=[jwt_cookie_auth.on_app_init],
    plugins=[sqlalchemy_plugin],
    logging_config=logging_config,
)

if __name__ == '__main__':
    uvicorn.run("src.app.main:app", host="localhost", port=8000, reload=True)
