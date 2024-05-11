from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    previlage = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    photo_path = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
    
class LostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(512))
    tags = db.Column(db.String(128))
    photo_paths = db.Column(db.String(128))
    status = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   
    def __repr__(self):
        return '<LostItem {}>'.format(self.item_name)
    
class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claimer_description = db.Column(db.String(512))
    evidence_photo_paths = db.Column(db.String(512))
    admin_response = db.Column(db.String(512))
    status = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    item_id = db.Column(db.Integer, db.ForeignKey('lost_item.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    claimer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Claim {}>'.format(self.item_id)
    
