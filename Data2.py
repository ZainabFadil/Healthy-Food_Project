class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meals = relationship('Meal', back_populates='category')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    meal_id = Column(Integer, ForeignKey('meals.id'))
    
    user = relationship('User', back_populates='reviews')
    meal = relationship('Meal', back_populates='reviews')

class SubscriptionPlan(Base):
    __tablename__ = 'subscription_plans'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    duration_in_days = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship('UserSubscription', back_populates='subscription_plan')

class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    subscription_plan_id = Column(Integer, ForeignKey('subscription_plans.id'))
    
    user = relationship('User', back_populates='subscriptions')
    subscription_plan = relationship('SubscriptionPlan', back_populates='users')

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Pending")
    
    user_id = Column(Integer, ForeignKey('users.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    subscription_id = Column(Integer, ForeignKey('user_subscriptions.id'))
    
    user = relationship('User', back_populates='payments')
    order = relationship('Order', back_populates='payments')
    subscription = relationship('UserSubscription', back_populates='payments')

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='addresses')

class Coupon(Base):
    __tablename__ = 'coupons'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    discount_percentage = Column(Float)
    discount_amount = Column(Float)
    expiry_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    orders = relationship('Order', back_populates='coupon')

# Update relationships in existing models
class Meal(Base):
    __tablename__ = 'meals'
    # existing fields...
    
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='meals')
    
    reviews = relationship('Review', back_populates='meal')

class User(Base):
    __tablename__ = 'users'
    # existing fields...
    
    reviews = relationship('Review', back_populates='user')
    subscriptions = relationship('UserSubscription', back_populates='user')
    payments = relationship('Payment', back_populates='user')
    addresses = relationship('Address', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'
    # existing fields...
    
    payments = relationship('Payment', back_populates='order')
    coupon_id = Column(Integer, ForeignKey('coupons.id'))
    coupon = relationship('Coupon', back_populates='orders')
