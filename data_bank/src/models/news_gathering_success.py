from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class NewsGatheringSuccess(Base):
    __tablename__ = 'news_gathering_success'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('news_gathering_events.id', ondelete='CASCADE'), nullable=True)
    event: Mapped[Text] = mapped_column(Text(), nullable=False, unique=False)
    details: Mapped[Text] = mapped_column(Text(), nullable=False, unique=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
