from typing import List, Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    store_id: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class config:
        orm_mode = True
