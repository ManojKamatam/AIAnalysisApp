import time
import random
from app import redis_client
from app.database import Product, Order, db
import logging

logger = logging.getLogger(__name__)

class InventoryService:
@staticmethod
def check_stock(product_id):
product = Product.query.get(product_id)
if not product:
raise ValueError("Product not found")
return product.stock

@staticmethod
def update_stock(product_id, quantity):
product = Product.query.get(product_id)
if not product:
raise ValueError("Product not found")

if product.stock < quantity:
raise ValueError("Insufficient stock")

product.stock -= quantity
db.session.commit()

class OrderProcessor:
@staticmethod
def process_order(product_id, quantity):
try:
# Check cache first
cache_key = f"product_{product_id}"
cached_stock = redis_client.get(cache_key)

if not cached_stock:
stock = InventoryService.check_stock(product_id)
redis_client.setex(cache_key, 300, str(stock))
else:
stock = int(cached_stock)

if stock < quantity:
raise ValueError("Insuffic... [Response truncated for size]