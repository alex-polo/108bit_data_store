from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .news_gathering_events import NewsGatheringEvents
from .queue_output_news_package import QueueOutputNewsPackage


class NewsPosts(Base):
    __tablename__ = "news_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    grubber_event_id: Mapped[int] = mapped_column(ForeignKey(NewsGatheringEvents.id, ondelete='CASCADE'), nullable=True,
                                                  unique=False)
    # = Column(Integer,
    #                       ForeignKey('grubber_events.id', ondelete='CASCADE'), nullable=True)

    date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, unique=False)
    title: Mapped[Text] = mapped_column(Text(), nullable=False, unique=False)
    details: Mapped[Text] = mapped_column(Text(), nullable=False, unique=False)
    more: Mapped[Text] = mapped_column(Text(), nullable=False, unique=False)
    image_url: Mapped[Text] = mapped_column(Text(), nullable=True, unique=False)
    main_tag: Mapped[str] = mapped_column(String(255), nullable=True, unique=False)
    field_tags: Mapped[str] = mapped_column(String(255), nullable=True, unique=False)
    author: Mapped[str] = mapped_column(String(255), nullable=True, unique=False)
    owner: Mapped[str] = mapped_column(String(30), nullable=False, unique=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    queue_output_package = relationship(QueueOutputNewsPackage, passive_deletes=True)
