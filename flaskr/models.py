from sqlalchemy import Column, Integer, String
from flaskr.database import Base
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
#from flaskr import db

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    pw_hash = Column(String(80))

    def __init__(self, email=None, pw_hash=None):
        self.email = email
        self.pw_hash = pw_hash
    def __repr__(self):
        return f'<User {self.email!r}>'