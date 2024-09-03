from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class NewsGatheringEvents(Base):
    __tablename__ = "news_gathering_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    site_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_gathering.id', ondelete='CASCADE'), nullable=True)
    event: Mapped[str] = mapped_column(String(50), nullable=False, unique=False)
    is_success: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
