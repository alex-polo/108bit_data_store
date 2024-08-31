from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
