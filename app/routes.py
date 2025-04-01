from flask import Blueprint, jsonify, request
from app.services import InventoryService, OrderProcessor
from app.database import Product
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

@main.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'stock': p.stock
        } for p in products])
    except Exception as e:
        logger.exception("Error fetching products")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        order_id = OrderProcessor.process_order(
            data['product_id'],
            data['quantity']
        )
        return jsonify({'order_id': order_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.exception("Error creating order")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/stock/<int:product_id>', methods=['GET'])
def check_stock(product_id):
    try:
        stock = InventoryService.check_stock(product_id)
        return jsonify({'stock': stock})
    except Product.DoesNotExist:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        logger.exception("Error checking stock")
        return jsonify({'error': 'Internal server error'}), 500