import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://flaskuser:flaskpass@localhost/flaskdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False