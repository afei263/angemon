# -*- coding: utf-8 -*-

from MySQLdb import ProgrammingError
from markdown import markdown

from base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        try:
            entries = self.db.query("SELECT * FROM Entry ORDER BY PublishTime DESC LIMIT 5")
        except ProgrammingError:
            self.redirect("/install")
            return
        for entry in entries:
            entry.Markdown = markdown(entry.Content)
        self.render('index.html', entries = entries)
