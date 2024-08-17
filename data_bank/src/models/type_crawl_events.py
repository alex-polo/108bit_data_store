
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TypeCrawlEvent(Base):
    __tablename__ = "type_crawl_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
