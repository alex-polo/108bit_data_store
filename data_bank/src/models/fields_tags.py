
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class FieldTag(Base):
    __tablename__ = "fields_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    field_tag_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=False)
