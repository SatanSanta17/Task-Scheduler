from flask import Flask
from flask_pymongo import PyMongo
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    
    # Access the environment variable
    mongo_uri = os.environ.get('MONGO_URL')

    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['MONGO_URI'] = mongo_uri
    mongo.init_app(app)
    
        
    @app.template_filter('format_date')
    def format_date(value):
        """Format a date as mm/dd/yyyy."""
        date_obj = datetime.strptime(value, '%Y-%m-%d')
        return date_obj.strftime('%m/%d/%Y')

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    
    # Register the filter with the app
    app.jinja_env.filters['format_date'] = format_date

    return app
