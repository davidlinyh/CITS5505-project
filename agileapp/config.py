import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ITEM_PHOTO_FOLDER = os.path.join(basedir, os.path.join(os.path.join('app', 'static'), 'item_photos'))
    EVIDENCE_PHOTO_FOLDER = os.path.join(basedir, os.path.join(os.path.join('app', 'static'), 'evidence_photos'))
    PROFILE_PHOTO_FOLDER = os.path.join(basedir, os.path.join(os.path.join('app', 'static'), 'profile_photos'))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lost-and-never-found'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
