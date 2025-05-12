import os
import logging
from enum import Enum

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment or config
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7564053348:AAFKcZjHsgOl34ndJH5-LsDBTD-rOKxA7Bs')
BOT_TOKEN = TOKEN  # Дополнительный вариант имени переменной

# Admin IDs (строки для корректного сравнения с telegram_id)
ADMIN_IDS = ["7961024553"]  # Default admin ID
NOTIFICATION_CHAT_ID = "-4610332724"  # Chat ID for notifications с минусом для групп

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

# User roles
class UserRole(Enum):
    USER = "user"
    OPERATOR = "operator"
    ADMIN = "admin"

# Order status
class OrderStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Order types
class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"

# Referral system tiers
REFERRAL_TIERS = {
    0: 0.10,   # 0-10 referrals: 10%
    10: 0.125, # 10-25 referrals: 12.5%
    25: 0.15,  # 25-50 referrals: 15%
    50: 0.175, # 50-100 referrals: 17.5%
    100: 0.20  # 100+ referrals: 20%
}

# Default rates (will be updated by admins)
DEFAULT_RATES = {
    "ltc_usd_buy": 65.0,     # USD price to buy 1 LTC
    "ltc_usd_sell": 63.0,    # USD price to sell 1 LTC
    "usd_rub_buy": 90.0,     # RUB price to buy 1 USD
    "usd_rub_sell": 88.0     # RUB price to sell 1 USD
}

# Command descriptions
COMMANDS = {
    'start': 'Начать работу с ботом',
    'help': 'Показать помощь',
    'profile': 'Ваш профиль',
    'referral': 'Реферальная система',
    'rates': 'Текущие курсы',
    'buy': 'Создать заявку на покупку LTC',
    'sell': 'Создать заявку на продажу LTC',
    'orders': 'Ваши заявки',
    'balance': 'Ваш баланс',
    'active_orders': 'Активные заявки (для операторов)',
    'set_rates': 'Установить курсы (для админов)',
    'users': 'Управление пользователями (для админов)',
    'broadcast': 'Создать рассылку (для админов)',
    'stats': 'Статистика (для админов)',
    'commands': 'Управление командами (для админов)'
}
