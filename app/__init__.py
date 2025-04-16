from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging
import redis

# Initialize Flask extensions
db = SQLAlchemy()
redis_client = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Initialize Redis
    global redis_client
    redis_client = redis.Redis.from_url(app.config['REDIS_URL'])

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )

    # Create database tables
    with app.app_context():
        db.create_all()

    return app