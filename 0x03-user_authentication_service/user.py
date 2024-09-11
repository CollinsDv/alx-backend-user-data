#!/usr/bin/env python3
"""SQLAlchemy model implementation
"""
from sqlalchemy import Column, Integer, String

Base = __import__('base').Base


class User(Base):
    """defines a user table map to the database
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
