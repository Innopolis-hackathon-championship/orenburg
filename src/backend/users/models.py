import datetime

from sqlalchemy import Column, ForeignKey, String, Integer, Float, Enum, DateTime, Boolean

from database import Base
from .constants import *


class User(Base):
    __tablename__ = 'user'
    
    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    fullname = Column("fullname", String)
    telegram_id = Column('telegram_id', String)
    role = Column(Enum(Role))
    joined = Column('joined', DateTime, default=datetime.datetime.now)
    balance = Column("balance", Float, default=False)
    is_verified = Column("is_confirmed", Boolean, default=False)
    code = Column("code", String(length=5))
    
    # Django requirements
    last_login = Column('last_login', DateTime, default=datetime.datetime.now)
    password = Column("password", String)
    is_active = Column("is_active", Boolean, default=False)
    is_superuser = Column("is_superuser", Boolean, default=False)
    
    
    __mapper_args__ = {
        "polymorphic_on": "role",
        # "polymorphic_identity": "user",
    }
    
    def verify(self, code: str):
        if self.is_verified:
            return True
        if self.code != code:
            return False
        self.is_verified = True
        return True
        

class Customer(User):
    __tablename__ = 'customer'
    
    id = Column('id', ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": Role.customer,
    }


class Courier(User):
    __tablename__ = 'courier'
    
    id = Column('id', ForeignKey('user.id'), primary_key=True)    
    is_online = Column('is_online', Boolean)
    raiting = Column("raiting", Float, default=5)
    is_delivering = Column("is_delivering", Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_identity": Role.courier,
    }


class Barmaid(User):
    __tablename__ = 'barmaid'
    
    id = Column('id', ForeignKey('user.id'), primary_key=True)    
    
    __mapper_args__ = {
        "polymorphic_identity": Role.barmaid,
    }
    

class Admin(User):
    __tablename__ = 'admin'
    
    id = Column('id', ForeignKey('user.id'), primary_key=True)    
    __mapper_args__ = {
        "polymorphic_identity": Role.admin,
    }


role_map = {
    Role.customer: Customer,
    Role.courier: Courier,
    Role.barmaid: Barmaid,
    Role.admin: Admin
}
