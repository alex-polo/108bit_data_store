from typing import Optional

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class CatalogsCategory(Base):
    __tablename__ = "catalog_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    url: Mapped[Optional[str]] = mapped_column(String(300), nullable=False, unique=False)
