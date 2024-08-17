from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Scheduler(Base):
    __tablename__ = "scheduler"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
