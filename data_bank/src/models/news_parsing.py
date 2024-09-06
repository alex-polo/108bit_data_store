
from typing import Optional, List

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .schemes_parser import Parser
from .news_gathering_events import NewsGatheringEvents


class NewsGathering(Base):
    __tablename__ = "news_gathering"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=False)
    url: Mapped[Optional[str]] = mapped_column(String(300), nullable=False, unique=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    vendor: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    field_tags: Mapped[Optional[str]] = mapped_column(String(1024), unique=False)
    is_enable: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)
    parser_id: Mapped[int] = mapped_column(ForeignKey(Parser.id), nullable=True, unique=False)
    parser: Mapped["Parser"] = relationship()

    grubber_events = relationship(NewsGatheringEvents, passive_deletes=True)
