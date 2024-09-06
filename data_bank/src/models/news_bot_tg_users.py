from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TgUser(Base):
    __tablename__ = "tg_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=True, unique=True)
    tg_bot: Mapped[Optional[str]] = mapped_column(String(150), unique=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), unique=False)
    second_name: Mapped[Optional[str]] = mapped_column(String(50), unique=False)
    surname: Mapped[Optional[str]] = mapped_column(String(50), unique=False)
    phone_number_tg: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=True)
    update_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now())
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now)
