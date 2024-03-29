#!/usr/bin/python3
""" Holds class Admin """

from re import I
from models import storage_type
from models.base_model import BaseModel, Base
from os import getenv
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String, null


class Admin(UserMixin, BaseModel, Base):
    """ Representation of admin """
    if storage_type == "db":
        __tablename__ = 'admins'
        id = Column(String(60), nullable=False, primary_key=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(60), nullable=False)
        last_name = Column(String(60), nullable=False)
        date_of_birth = Column(String(10), nullable=False)
        nin = Column(Integer, nullable=False, unique=True)
        phone_number = Column(Integer, nullable=False, unique=True)
        email = Column(String(128), nullable=False, unique=True)
        role = Column(String(128), nullable=False)
    else:
        def __init__(self, *args, **kwargs):
            """ Initializes admin
            """
            super().__init__(*args, **kwargs)
