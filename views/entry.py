# -*- coding: utf-8 -*-

from tornado.web import HTTPError

from views.base import BaseHandler
from models.entry import EntryHelper

class EntryHandler(BaseHandler, EntryHelper):
    def get(self, slug):
        entry = self.select_entry_by_slug(slug)
        if not entry:
            raise HTTPError(404)
        self.render("entry.html", entry = entry)
