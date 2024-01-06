import os

class Config:
    SECRET_KEY = '10be645508f6044194986e98faf269b8'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False