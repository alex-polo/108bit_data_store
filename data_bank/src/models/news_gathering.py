
from typing import Optional, List

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .parser import Parser


class NewsGathering(Base):
    __tablename__ = "news_gathering"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    vendor: Mapped[Optional[str]] = mapped_column(String(255), unique=False)
    field_tags: Mapped[Optional[str]] = mapped_column(String(1024), unique=False)
    is_enable: Mapped[bool] = mapped_column(Boolean, nullable=False, unique=False, default=False)
    # parser_id: Mapped[int] = mapped_column(ForeignKey("parsers.id"))
    parser_id: Mapped[int] = mapped_column(ForeignKey(Parser.id), nullable=True, unique=False)
    parser: Mapped["Parser"] = relationship()

    # class Parent(Base):
    #     __tablename__ = "parent_table"
    #
    #     id: Mapped[int] = mapped_column(primary_key=True)
    #     child_id: Mapped[int] = mapped_column(ForeignKey("child_table.id"))
    #     child: Mapped["Child"] = relationship()




