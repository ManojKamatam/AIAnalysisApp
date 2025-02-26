from app import create_app, db
from app.database import Product
import random

def init_db():
    app = create_app()
    with app.app_context():
        # Create tables
        db.create_all()

        # Add sample products
        products = [
            Product(name='Laptop', price=999.99, stock=50),
            Product(name='Smartphone', price=499.99, stock=100),
            Product(name='Headphones', price=99.99, stock=200),
            Product(name='Tablet', price=299.99, stock=75),
            Product(name='Smartwatch', price=199.99, stock=150)
        ]

        for product in products:
            db.session.add(product)

        db.session.commit()

if __name__ == '__main__':
    init_db()
