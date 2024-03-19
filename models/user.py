#!/usr/bin/python3
""" User inherits from BaseModel and Base (respect the order) """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import validates

class User(BaseModel, Base):
     """This class defines a user by various attributes"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Invalid email address."
        return email

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) >= 8, "Password must be at least 8 characters long."
        return password
