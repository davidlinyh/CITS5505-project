from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship,declarative_base
from datetime import datetime

Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    photo_path = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class LostItems(Base):
    __tablename__ = 'LostItems'
    item_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    tag = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey('Users.user_id'))
    status = Column(String, nullable=False, default='Available')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class Claims(Base):
    __tablename__ = 'Claims'
    claim_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('LostItems.item_id'))
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    status = Column(String, nullable=False, default='Pending')
    evidence = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

class AdminActions(Base):
    __tablename__ = 'AdminActions'
    action_id = Column(Integer, primary_key=True)
    claim_id = Column(Integer, ForeignKey('Claims.claim_id'))
    admin_id = Column(Integer, ForeignKey('Users.user_id'))
    action = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

class LostItemPosts(Base):
    __tablename__ = 'LostItemPosts'
    post_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('LostItems.item_id'))
    admin_id = Column(Integer, ForeignKey('Users.user_id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

engine = create_engine('sqlite:///C:/Users/adhar/Desktop/sem3/cits5505/Group project/CITS5505-project/Database/main.db')
 
Base.metadata.create_all(engine)
