
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class VendorTag(Base):
    __tablename__ = "vendors_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vendor_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=False)
