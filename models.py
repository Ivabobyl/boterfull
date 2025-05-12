import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid

from config import DATABASE_URL, UserRole, OrderStatus, OrderType, logger

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    referral_code = Column(String(20), unique=True)
    referred_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # Relationships
    referrals = relationship("User", foreign_keys=[referred_by])
    orders = relationship("Order", back_populates="user", foreign_keys="Order.user_id")
    operated_orders = relationship("Order", back_populates="operator", foreign_keys="Order.operator_id")
    
    def __init__(self, telegram_id, username=None, first_name=None, last_name=None):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.referral_code = str(uuid.uuid4())[:8]

    def get_full_name(self):
        if self.first_name is not None and self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name is not None:
            return self.first_name
        elif self.username is not None:
            return self.username
        return f"User {self.telegram_id}"
    
    def get_referral_count(self, session):
        return session.query(User).filter(User.referred_by == self.id).count()


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_number = Column(String(10), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    operator_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    type = Column(Enum(OrderType), nullable=False)
    amount_rub = Column(Float, nullable=False)
    amount_ltc = Column(Float, nullable=True)
    rate_ltc_usd = Column(Float, nullable=True)
    rate_usd_rub = Column(Float, nullable=True)
    spread = Column(Float, nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="orders", foreign_keys=[user_id])
    operator = relationship("User", back_populates="operated_orders", foreign_keys=[operator_id])
    
    def __init__(self, user_id, type, amount_rub, amount_ltc=None, rate_ltc_usd=None, rate_usd_rub=None):
        self.user_id = user_id
        self.type = type
        self.amount_rub = amount_rub
        self.amount_ltc = amount_ltc
        self.rate_ltc_usd = rate_ltc_usd
        self.rate_usd_rub = rate_usd_rub
        self.order_number = f"Z{str(uuid.uuid4())[:6].upper()}"


class Rate(Base):
    __tablename__ = 'rates'
    
    id = Column(Integer, primary_key=True)
    ltc_usd_buy = Column(Float, nullable=False)  # Price to buy 1 LTC in USD
    ltc_usd_sell = Column(Float, nullable=False)  # Price to sell 1 LTC in USD
    usd_rub_buy = Column(Float, nullable=False)  # Price to buy 1 USD in RUB
    usd_rub_sell = Column(Float, nullable=False)  # Price to sell 1 USD in RUB
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_by = Column(Integer, ForeignKey('users.id'), nullable=True)


class CustomCommand(Base):
    __tablename__ = 'custom_commands'
    
    id = Column(Integer, primary_key=True)
    command = Column(String(50), nullable=False, unique=True)
    response_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    is_active = Column(Boolean, default=True)


class ReferralBonus(Base):
    __tablename__ = 'referral_bonuses'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    referral_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    amount = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    referral = relationship("User", foreign_keys=[referral_id])
    order = relationship("Order")


# Database setup
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    
    # Создаем таблицы, если они не существуют
    Base.metadata.create_all(engine)  # Создаем или обновляем таблицы
    
    Session = sessionmaker(bind=engine)
else:
    logger.error("DATABASE_URL environment variable is not set")
    raise ValueError("DATABASE_URL environment variable is not set")
