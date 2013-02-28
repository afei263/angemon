# -*- coding: utf-8 -*-

from views.base import BaseHandler

from models.entry import Entry
from models.entry import EntryHelper

class IndexHandler(BaseHandler, EntryHelper):
    def get(self):
        if self.current_user:
            entries = self.select_entries(draft = True)
        else:
            entries = self.select_entries()
        self.render('index.html', entries = entries)
