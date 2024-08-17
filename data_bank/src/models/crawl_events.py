
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CrawlEvent(Base):
    __tablename__ = "crawl_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)





