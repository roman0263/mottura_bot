from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from bot.database.db import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(300))
    price = Column(Float, nullable=False)
    category = Column(String(50), index=True)

    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}')"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50))
    last_name = Column(String(50), nullable=True)

    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")