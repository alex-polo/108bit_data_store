from typing import Optional

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SchemeParser(Base):
    __tablename__ = "schemes_parsers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    system_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    parser_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=False, unique=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    parser_type: Mapped[Optional[str]] = mapped_column(String(150), unique=False)
    is_enable: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)
    is_parser_scheme_missing: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)
