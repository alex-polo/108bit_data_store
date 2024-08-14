from typing import Optional

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Parser(Base):
    __tablename__ = "parsers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    system_name: Mapped[int] = mapped_column(String(255), nullable=False, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    type_parser: Mapped[Optional[str]] = mapped_column(String(150), unique=False)
    is_enable: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)
