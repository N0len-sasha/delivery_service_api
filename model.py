from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from db_setup import Base

class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = Mapped[str]
    weight = Mapped[float]
    price = Mapped[float]