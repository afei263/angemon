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


class FeedHandler(BaseHandler, EntryHelper):
    def get(self):
        entries = self.select_entries()
        self.set_header("Content-Type", "application/atom+xml; charset=utf-8")
        self.render("feed.xml", entries = entries, max_update = reduce(max, [e.updateTime for e in entries]), request = self.request)
