from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class QueueOutputNewsPackage(Base):
    __tablename__ = "queue_output_news_package"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    value: Mapped[str] = mapped_column(String(255), unique=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_posts.id', ondelete='CASCADE'), nullable=True)
    status: Mapped[str] = mapped_column(String(25), nullable=False, unique=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
