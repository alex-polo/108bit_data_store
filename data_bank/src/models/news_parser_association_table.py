from sqlalchemy import Table, Column, ForeignKey

from .base import Base

news_parser_association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("left_table.id")),
    Column("right_id", ForeignKey("right_table.id")),
)


# class Parent(Base):
#     __tablename__ = "left_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[List[Child]] = relationship(secondary=association_table)
#
#
# class Child(Base):
#     __tablename__ = "right_table"
#
#     id: Mapped[int] = mapped_column(primary_key=True)