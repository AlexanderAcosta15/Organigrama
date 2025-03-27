import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-segura-123'
    SQLALCHEMY_DATABASE_URI = 'postgresql+pg8000://postgres:2004@localhost:5433/organigrama_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False