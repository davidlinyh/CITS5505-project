import os
import secrets
basedir = os.path.abspath(os.path.dirname(__file__))

def generate_secret_key():
    return secrets.token_hex(32)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or generate_secret_key()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
