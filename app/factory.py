from flask import Flask
from flask_pymongo import PyMongo
import os

mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['MONGO_URI'] = 'mongodb+srv://burhanuddinchital25151:ndNlk0EKhr7kwz3W@tasks.p2zch6w.mongodb.net/tasks'

    mongo.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
