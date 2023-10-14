import datetime
from pydantic import BaseModel

from .constants import OrderStatus


class ORMMixin:
    model_config = {
        'from_attributes': True
    }
    

class Product(ORMMixin, BaseModel):
    id: int
    name: str
    quantity: int
    image: str
    is_visible: bool
    price: float


class CreateProduct(BaseModel):
    name: str
    quantity: int
    image: str = None
    is_visible: bool = True
    price: float


class Order(ORMMixin, BaseModel):
    id: int
    customer_id: int
    status: OrderStatus
    start_date: datetime.datetime
    finish_date: datetime.datetime | None = None
    amount: float
    code: str


class ProductInCart(BaseModel):
    id: int
    amount: int


class CreateOrder(BaseModel):
    customer_username: str
    products: list[ProductInCart]
    delivery_address: str
    
