from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import Mapped

from src.app.database.setup_db import Base, dto_factory


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, unique=True)
    password: Mapped[str] = Column(String)


UserCreateOrLoginDTO = dto_factory("UserCreateDTO", User, exclude=["id"])
UserGetDTO = dto_factory("UserGetDTO", User, exclude=["password"])
