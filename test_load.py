import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'http://localhost:5000'

def generate_load():
    while True:
        try:
            # Get products
            response = requests.get(f"{BASE_URL}/api/products")
            products = response.json()

            if products:
                # Create random order
                product = random.choice(products)
                order_data = {
                    'product_id': product['id'],
                    'quantity': random.randint(1, 5)
                }
                requests.post(f"{BASE_URL}/api/orders", json=order_data)

            # Check stock for random product
            product_id = random.randint(1, 5)
            requests.get(f"{BASE_URL}/api/stock/{product_id}")

            # Random sleep between requests
            time.sleep(random.uniform(0.1, 1.0))

        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(1)

if __name__ == '__main__':
    # Create multiple threads to generate load
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(5):
            executor.submit(generate_load)
