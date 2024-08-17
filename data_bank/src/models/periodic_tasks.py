from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PeriodicTasks(Base):
    __tablename__ = "periodic_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
