import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
import logging
from functools import wraps

BASE_URL = 'http://localhost:5000'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def retry_with_exponential_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = base_delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Request failed: {str(e)}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    retries += 1
                    delay *= 2
            
            logger.error(f"Request failed after {max_retries} retries. Giving up.")
            raise Exception("Max retries exceeded")
        
        return wrapper
    
    return decorator

@retry_with_exponential_backoff()
def get_products():
    response = requests.get(f"{BASE_URL}/api/products")
    response.raise_for_status()
    return response.json()

@retry_with_exponential_backoff()
def create_order(order_data):
    response = requests.post(f"{BASE_URL}/api/orders", json=order_data)
    response.raise_for_status()

@retry_with_exponential_backoff()
def check_stock(product_id):
    response = requests.get(f"{BASE_URL}/api/stock/{product_id}")
    response.raise_for_status()

def generate_load():
    while True:
        try:
            products = get_products()

            if products:
                product = random.choice(products)
                order_data = {
                    'product_id': product['id'],
                    'quantity': random.randint(1, 5)
                }
                create_order(order_data)

            product_id = random.randint(1, 5)
            check_stock(product_id)

            time.sleep(random.uniform(0.1, 1.0))

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            time.sleep(1)

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(5):
            executor.submit(generate_load)