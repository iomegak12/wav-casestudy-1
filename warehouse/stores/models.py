from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from ..common import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True)
    items = relationship(
        "Item",
        primaryjoin="Store.id == Item.store_id",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Store(name={self.name})"
