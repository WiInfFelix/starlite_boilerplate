from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import Mapped
from starlite import Partial

from src.app.database.models.base_model import BaseModel
from src.app.database.setup_db import Base, dto_factory


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = Column(String, unique=True)
    email: Mapped[str] = Column(String, unique=True)
    password: Mapped[str] = Column(String)


UserCreateDTO = dto_factory("UserCreateDTO", User, exclude=["id", "created_at", "updated_at"])
UserLoginDTO = dto_factory("UserLoginDTO", User, exclude=["id", "name", "created_at", "updated_at"])
UserGetDTO = dto_factory("UserGetDTO", User, exclude=["password"])
UserUpdateDTO = Partial[dto_factory("UserUpdateDTO", User, exclude=["id", "password", "created_at", "updated_at"])]
