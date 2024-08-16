
from typing import Optional

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class InternetSite(Base):
    __tablename__ = "internet_sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    parser: Mapped[Optional[str]] = mapped_column(String(150), unique=False)
    is_enable: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)

    # vendor: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    # field_tags: ['#Системы_автоматики', ]
