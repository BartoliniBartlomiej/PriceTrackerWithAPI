from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

engine = create_engine('sqlite:///prices.db', echo=False)
Session = sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    #jeden produkt ma wiele wpisów cen
    prices = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="prices")

def init_db():
    Base.metadata.create_all(engine)