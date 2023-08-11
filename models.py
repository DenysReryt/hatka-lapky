"""
Module containing SQLAlchemy models.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from flask_login import UserMixin


db = SQLAlchemy()
migrate: Migrate = Migrate()

class UserModel(db.Model):
    """ User model """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.BigInteger(), nullable=False, unique=True)
    date = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    last_message = db.Column(db.String(), nullable=False)
    messages = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    
    def to_dict(self):
        """ Return the model properties as a dictionary """
        
        return {
            'id': self.id,
            'first_name': self.first_name,
            'username': self.username,
            'user_id': self.user_id,
            'date': self.date,
            'last_message': self.last_message,
            'messages': self.messages,
            'active': self.active
        }


class AdminModel(UserMixin, db.Model):
    """ Admin model """
    
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    
    def to_dict(self):
        """ Return the model properties as a dictionary """
        
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
            
        }
    
    