from flask import Flask
from flask_pymongo import PyMongo
from datetime import datetime
import os

mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['MONGO_URI'] = 'mongodb+srv://burhanuddinchital25151:ndNlk0EKhr7kwz3W@tasks.p2zch6w.mongodb.net/tasks'

    mongo.init_app(app)
    
        
    @app.template_filter('format_date')
    def format_date(value):
        """Format a date as mm/dd/yyyy."""
        date_obj = datetime.strptime(value, '%Y-%m-%d')
        return date_obj.strftime('%m/%d/%Y')

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    
    # # Register the filter with the app
    # app.jinja_env.filters['format_date'] = format_date

    return app
