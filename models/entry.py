# -*- coding: utf-8 -*-

import re
import logging
import markdown
import unidecode

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
from models.utils import protect_one

class Entry(Base, baseModule):
    __tablename__ = 'Entry'
    title = Column(UnicodeText)
    content = Column(UnicodeText)
    markdown = Column(UnicodeText)
    author_id = Column(Integer, ForeignKey('User.id'))
    author = relation('User')
    slug = Column(String(255))
    draft = Column(Boolean)

    def __init__(self, title, content, author, slug, draft):
        self.title = unicode(title)
        self.content = unicode(content)
        self.author_id = author.id
        self.draft = draft
        
        if not slug:
            slug = unidecode.unidecode(unicode(title)).lower()
            slug = re.sub(r'\W+','-', slug)
        self.slug = slug

        self.markdown = unicode(markdown.markdown(content))

class EntryHelper(object):
    def select_entries(self, draft = False, limit = 5, offset = 0):
        query = self.db.query(Entry) \
                       .order_by(desc(Entry.createTime))
        if not draft:
            query = query.filter_by(draft = False)
        return query.offset(offset) \
                    .limit(limit) \
                    .all()
    def select_entry_by_id(self, pid):
        return self.db.query(Entry).get(pid)
    @protect_one
    def select_entry_by_slug(self, slug):
        slug = slug[:-1].lower()
        return self.db.query(Entry).filter_by(slug = slug).one()
