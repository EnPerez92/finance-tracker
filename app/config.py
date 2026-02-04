import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///finance_tracker.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
