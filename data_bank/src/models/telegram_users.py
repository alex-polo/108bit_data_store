from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_identifier: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, unique=False, nullable=False)
    type_bot: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), unique=False, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), unique=False, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=True)
    update_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now())
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now)