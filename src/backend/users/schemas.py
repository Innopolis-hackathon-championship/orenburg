import datetime

from pydantic import BaseModel

from .constants import *


class ORMMixin:
    model_config = {
        'from_attributes': True
    }
    

class UserRead(ORMMixin, BaseModel):
    id: int
    username: str
    fullname: str
    telegram_id: str
    role: Role
    balance: float
    joined: datetime.datetime
    is_verified: bool
    # model_config = {
    #     'from_attributes': True
    # }

class UserCreate(BaseModel):
    username: str
    fullname: str
    telegram_id: str
    role: Role = Role.customer


class UserUpdate(ORMMixin, BaseModel):
    username: str
    fullname: str
    telegram_id: str


class CustomerRead(UserRead):
    pass




class CustomerCreate(UserCreate):
    pass


class UnverifiedUser(BaseModel):
    username: str
    fullname: str
    code: str
    
    
class Courier(UserRead):
    rating: float
    is_online: bool