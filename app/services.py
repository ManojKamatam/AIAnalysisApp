import time
import random
from app import redis_client
from app.database import Product, Order, db
import logging
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class InventoryService:
@staticmethod
def check_stock(product_id):
# Check cache first to avoid unnecessary DB queries
cache_key = f"... [Response truncated for size]