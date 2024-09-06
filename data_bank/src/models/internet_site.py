
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class InternetSite(Base):
    __tablename__ = "internet_sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    # news_gathering
    # catalog_gathering
    # information_gathering
