
from typing import Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class InternetSite(Base):
    __tablename__ = "internet_sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    news_gathering_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_gathering.id'), nullable=True)
    news_gathering: Mapped['NewsGathering'] = relationship(back_populates="internet_site")

    catalog_gathering_id: Mapped[int] = mapped_column(Integer, ForeignKey('catalog_gathering.id'), nullable=True)
    catalog_gathering: Mapped['CatalogGathering'] = relationship(back_populates="internet_site")

    # news_gathering
    # catalog_gathering
    # information_gathering
