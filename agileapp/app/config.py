import os
import secrets
basedir = os.path.abspath(os.path.dirname(__file__))

def generate_secureKey(length=50):
    return secrets.token_hex(length)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or generate_secureKey()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
