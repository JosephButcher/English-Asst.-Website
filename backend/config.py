import os

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')  # Change this for production
    DEBUG = os.environ.get('FLASK_DEBUG', True)

    # Database configuration
    DB_DRIVER = os.environ.get('DB_DRIVER', 'SQL Server')
    DB_SERVER = os.environ.get('DB_SERVER', 'MCN110-LHN7M2BB')  # Replace with your server name
    DB_NAME = os.environ.get('DB_NAME', 'EnglishAssistant')
    DB_CONNECTION_STRING = f"DRIVER={{{DB_DRIVER}}}; SERVER={DB_SERVER}; DATABASE={DB_NAME}"


config = Config()
