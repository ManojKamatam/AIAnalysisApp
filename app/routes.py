from flask import Blueprint, jsonify, request
from app import db
from app.database import Product, Order

main = Blueprint('main', __name__)

@main.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'stock': p.stock} for p in products])

@main.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']

    product = Product.query.get(product_id)
    if product and product.stock >= quantity:
        order = Order(product_id=product_id, quantity=quantity)
        product.stock -= quantity
        db.session.add(order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'})
    else:
        return jsonify({'message': 'Insufficient stock'}), 400

@main.route('/api/stock/<int:product_id>', methods=['GET'])
def get_stock(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'stock': product.stock})
    else:
        return jsonify({'message': 'Product not found'}), 404