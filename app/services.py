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
        try:
            product = Product.query.get(product_id)
            if not product:
                raise ValueError("Product not found")
            
            product.stock -= quantity
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating stock: {str(e)}", exc_info=True)
            raise

class OrderProcessor:
    @staticmethod
    def process_order(product_id, quantity):
        try:
            stock = InventoryService.check_stock(product_id)
            
            if stock < quantity:
                raise ValueError("Insufficient stock")
            
            # Create order
            order = Order(product_id=product_id, quantity=quantity)
            db.session.add(order)
            
            # Update stock
            InventoryService.update_stock(product_id, quantity)
            
            db.session.commit()
            return order.id
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error processing order: {str(e)}", exc_info=True)
            raise