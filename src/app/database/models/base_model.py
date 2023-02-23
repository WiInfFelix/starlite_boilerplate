import datetime

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import Mapped

from src.app.database.setup_db import Base


class BaseModel(Base):
    __abstract__ = True
    __tablename__ = __name__.lower()

    id: Mapped[int] = Column(Integer, primary_key=True)
    created_at: Mapped[datetime.datetime] = Column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime.datetime] = Column(DateTime, onupdate=func.now())
