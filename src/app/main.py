import uvicorn
from sqlalchemy import Column, Float, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, declarative_base

from starlite import DTOFactory, HTTPException, Starlite, get, post
from starlite.plugins.sql_alchemy import SQLAlchemyConfig, SQLAlchemyPlugin
from starlite.status_codes import HTTP_404_NOT_FOUND

from src.app.controllers.user_controller import UserController
from src.app.database.setup_db import on_startup, sqlalchemy_plugin

app = Starlite(
    route_handlers=[UserController],
    on_startup=[on_startup],
    plugins=[sqlalchemy_plugin],
)

if __name__ == '__main__':
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8000, reload=True)
