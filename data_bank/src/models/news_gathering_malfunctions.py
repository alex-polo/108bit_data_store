from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class NewsGatheringMalfunctions(Base):
    __tablename__ = 'news_gathering_malfunctions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('news_gathering_events.id', ondelete='CASCADE'), nullable=True)
    malfunction_type: Mapped[str] = mapped_column(String(50), nullable=False, unique=False)
    malfunction_details: Mapped[str] = mapped_column(String(100), nullable=False, unique=False)
    service_name: Mapped[str] = mapped_column(String(150), nullable=True, unique=False, default=None)
    module_name: Mapped[str] = mapped_column(String(100), nullable=True, unique=False, default=None)
    source: Mapped[str] = mapped_column(String(255), nullable=False, unique=False)
    date: Mapped[DateTime] = mapped_column(DateTime(), nullable=False, unique=False)
    title: Mapped[str] = mapped_column(String(255), nullable=True, unique=False, default=None)
    description: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    text_error: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    text_details: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    image_url: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    attribute_1: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    attribute_2: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    attribute_3: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    attribute_4: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    attribute_5: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False, default=None)
    created_on: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)

    # queue_output_news_package = relationship(QueueOutputNewsPackage, passive_deletes=True)
