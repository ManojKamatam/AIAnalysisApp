import time
import random
from app import redis_client
from app.database import Product, Order, db
import logging

logger = logging.getLogger(__name__)

class InventoryService:
@staticmethod
def check_stock(product_id):
# Cache product stock to avoid repetitive database queries
cache_key = f"product_stock_{product_id}"
cached_stock = redis_client.get(cache_key)

if cached_stock:
return int(cached_stock)

# Only perform the database query if not in cache
product = Product.query.get(product_id)
if not product:
raise ValueError("Product not found")

# Cache the result for 1 minute
redis_client.setex(cache_key, 60, str(product.stock))
return product.stock

@staticmethod
def update_stock(product_id, quantity):
try:
# Use query with update instead of fetching and modifying
result = Product.query.filter_by(id=product_id).update(
{"stock": Product.stock - quantity},
synchronize_se... [Response truncated for size]