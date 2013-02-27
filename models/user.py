# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import UnicodeText

from models.base import Base
from models.base import baseModule

class User(Base, baseModule):
    __tablename__ = 'User'
    username = Column(String(255))
    auth = Column(String(255))
    token = Column(String(255))
