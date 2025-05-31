from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    price = Column(Float, nullable=False)
    category = Column(String(50))

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"