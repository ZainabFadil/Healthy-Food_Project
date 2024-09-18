from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Many-to-Many relationship between Order and Meal
order_meal = Table('order_meal', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('meal_id', Integer, ForeignKey('meals.id'), primary_key=True),
    Column('quantity', Integer, nullable=False, default=1)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meals = relationship('Meal', back_populates='user')
    orders = relationship('Order', back_populates='user')

class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    calories = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='meals')
    ingredients = relationship('Ingredient', back_populates='meal')
    orders = relationship('Order', secondary=order_meal, back_populates='meals')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    meal_id = Column(Integer, ForeignKey('meals.id'))
    meal = relationship('Meal', back_populates='ingredients')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False, default='Pending')
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
    meals = relationship('Meal', secondary=order_meal, back_populates='orders')

# Create an engine and database session
engine = create_engine('sqlite:///the_6_meals.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
