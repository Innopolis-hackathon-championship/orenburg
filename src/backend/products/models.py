from sqlalchemy import Column, String, Integer

from ..database import Base


class Product(Base):
    __tablename__ = 'product'
    
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    quantity = Column("quantity", Integer)
    image = Column("image", String)  # url на статику.
    is_visible = Column("is_visible")