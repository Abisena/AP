from pydantic import BaseModel
from typing import Optional

class comerce(BaseModel):
    name: str
    price: int
    quantity: int
    description: str
    category: str
    image: Optional[str]
    rating: float

class ItemUpdate(BaseModel):
    name: str
    price: float
    quantity: int
    description: str
    category: str
    image: Optional[str]
    rating: float
