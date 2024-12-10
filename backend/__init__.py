from flask import Flask
from flask_cors import CORS
import pyodbc
from backend.config import config

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)

    # Apply configurations
    app.config.from_object(config)

    # Database connection
    connection = pyodbc.connect(config.DB_CONNECTION_STRING)
    cursor = connection.cursor()

    # Register routes
    from backend.app import app as main_app
    app.register_blueprint(main_app)

    return app
