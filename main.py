# -*- coding: utf-8 -*-

from sqlalchemy import desc

from base import BaseHandler
from models import Entry

class IndexHandler(BaseHandler):
    def get(self):
        entries = self.session.query(Entry) \
                              .order_by(desc(Entry.PublishTime)) \
                              .limit(5) \
                              .all()
        self.render('index.html', entries = entries)
