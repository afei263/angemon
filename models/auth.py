# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import UnicodeText
from sqlalchemy.orm import relation

from models.base import Base
from models.base import baseModule

class Auth(Base, baseModule):
    __tablename__ = 'Auth'
    user_id = Column(Integer, ForeignKey("User.id"))
    user = relation("User")
    secret = Column(UnicodeText)

    def __init__(self, user, secret):
        self.user_id = user.id
        self.secret = secret

    def is_valid(self):
        now = datetime.datetime.now()
        delta = self.updateTime - now
        if delta.days > 30:
            return False
        return True

    def update_time(self, db):
        self.updateTime = datetime.datetime.now()
        db.add(self)
        db.commit()
