from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_setup import Base


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    weight: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    delivery_price: Mapped[float] = mapped_column(Float, nullable=True)

    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('types.id'))

    type: Mapped["Type"] = relationship("Type", back_populates="package", lazy="selectin")


class Type(Base):
    __tablename__ = "types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    package: Mapped["Package"] = relationship("Package", back_populates="type", lazy="selectin")

