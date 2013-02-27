# -*- coding: utf-8 -*-

from sqlalchemy import desc
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

class Entry(Base, baseModule):
    __tablename__ = 'Entry'
    title = Column(UnicodeText)
    content = Column(UnicodeText)
    markdown = Column(UnicodeText)
    author_id = Column(Integer, ForeignKey('User.id'))
    author = relation('User')
    slug = Column(String(255))

class EntryHelper(object):
    def select_entries(self, limit = 5, offset = 0):
        return self.db.query(Entry) \
                      .order_by(desc(Entry.createTime)) \
                      .offset(offset) \
                      .limit(limit) \
                      .all()
