import os

class Config:
    # Flask configuration
    # SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')  # Change this for production        ## secret key is only necessary for preventing hackers from stealing information
    # DEBUG = os.environ.get('FLASK_DEBUG', True)
    

    # # Database configuration
    # DB_DRIVER = os.environ.get('DB_DRIVER', 'SQL Server')
    # DB_SERVER = os.environ.get('DB_SERVER', 'MCN110-LHN7M2BB')  # Replace with your server name
    # DB_NAME = os.environ.get('DB_NAME', 'EnglishAssistant')
    # DB_CONNECTION_STRING = f"DRIVER={{{DB_DRIVER}}}; SERVER={DB_SERVER}; DATABASE={DB_NAME}"

    #less secure but easier implementation
    # Flask configuration
    SECRET_KEY = 'english_secret'  # This is a simple string for development
    DEBUG = True  # Keep debugging enabled during development

    # Database configuration
    DB_DRIVER = 'SQL Server'
    DB_SERVER = 'MCN110-LHN7M2BB'
    DB_NAME = 'EnglishAssistant'
    DB_CONNECTION_STRING = f"DRIVER={{{DB_DRIVER}}}; SERVER={DB_SERVER}; DATABASE={DB_NAME}"


config = Config()
