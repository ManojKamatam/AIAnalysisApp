import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
import logging

BASE_URL = 'http://localhost:5000'
MAX_RETRIES = 3
RETRY_DELAY = 1

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_load():
while True:
try:
# Get products
response = requests.get(f"{BASE_URL}/api/products")
if response.status_code == 200:
products = response.json()
if products:
# Create random order
product = random.choice(products)
order_data = {
'product_id': product['id'],
'quantity': random.randint(1, 5)
}
retries = 0
while retries < MAX_RETRIES:
order_response = requests.post(f"{BASE_URL}/api/orders", json=order_data)
if order_response.status_code == 201:
break
retries += 1
logger.warning(f"Order creation failed. Retry: {retries}/{MAX_RETRIES}")
time.sleep(RETRY_DELAY)
else:
logger.warning("No products found.")
else:
logger.error(f"Failed to get products. Status code: {response.status_code}")

# Check stock for random product
product_id = random.randint(1, 5)
stock_response = requests.get(f"{BASE_URL}/api/stock/{product_id}")
if stock_response.status_code == 200:
logger.info(f"Stock check successful for product ID: {product_id}")
else:
logger.warning(f"Stock check failed for product ID: {product_id}. Status code: {stock_response.status_code}")

# Random sleep between requests
time.sleep(random.uniform(0.1, 1.0))

except requests.exceptions.RequestException as e:
logger.error(f"Request error: {str(e)}")
time.sleep(1)

if __name__ == '__main__':
# Create multiple threads to generate load
with ThreadPoolExecutor(max_workers=5) as executor:
for _ in range(5):
executor.submit(generate_load)