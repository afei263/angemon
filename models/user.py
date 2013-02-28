# -*- coding: utf-8 -*-

import uuid
import binascii

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import UnicodeText

from models.base import Base
from models.base import baseModule
from models.auth import Auth
from models.utils import modify
from models.utils import protect_one

class User(Base, baseModule):
    __tablename__ = 'User'
    username = Column(String(255))
    password = Column(String(255))

    def __init__(self, username, hashed_password):
        self.username = username
        self.password = hashed_password
    
    def create_auth(self):
        random = binascii.b2a_hex(uuid.uuid4().bytes)
        return Auth(self, random)

class UserHelper(object):
    @protect_one
    def select_user_by_username(self, username):
        return self.db.query(User).filter_by(username = username).one()
