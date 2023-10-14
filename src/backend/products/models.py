import datetime
from sqlalchemy import Boolean, Column, Float, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from . import constants
from database import Base

class ProductToOrder(Base):
    __tablename__ = "product_to_order"
    
    id = Column("id", Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    amount = Column("amount", Integer)

class Product(Base):
    __tablename__ = 'product'
    
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    quantity = Column("quantity", Integer)
    image = Column("image", String, nullable=True)  # url на статику.
    is_visible = Column("is_visible", Boolean)
    price = Column("price", Float)
    
    # orders = relationship("Order", secondary="product_to_order", back_populates="products")
    

class Order(Base):
    __tablename__ = "order"
    id = Column("id", Integer, primary_key=True)
    customer_id = Column('customer_id', ForeignKey('user.id'))
    status = Column("status", Enum(constants.OrderStatus))
    delivery_address = Column("delivery_address", String)
    start_date = Column("start_date", DateTime, default=datetime.datetime.now)
    finish_date = Column("finish_date", DateTime, nullable=True, default=None)
    amount = Column("amount", Float, default=0)
    code = Column("code", String)
    
    products = relationship("Product", secondary="product_to_order")
