from flask import Blueprint, jsonify, request
from app import db, redis_client
from app.database import Product, Order

main = Blueprint('main', __name__)

@main.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_data = []
    for product in products:
        product_data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': product.stock
        })
    return jsonify(product_data)

@main.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']

    product = Product.query.get(product_id)
    if product.stock < quantity:
        return jsonify({'message': 'Insufficient stock'}), 400

    order = Order(product_id=product_id, quantity=quantity)
    db.session.add(order)

    product.stock -= quantity
    db.session.commit()

    return jsonify({'message': 'Order created successfully'})

@main.route('/api/stock/<int:product_id>', methods=['GET'])
def get_stock(product_id):
    stock = redis_client.get(f'stock_{product_id}')
    if stock is None:
        product = Product.query.get(product_id)
        if product:
            stock = product.stock
            redis_client.set(f'stock_{product_id}', stock)
        else:
            return jsonify({'message': 'Product not found'}), 404
    else:
        stock = int(stock)

    return jsonify({'stock': stock})