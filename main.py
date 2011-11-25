# -*- coding: utf-8 -*-

from MySQLdb import ProgrammingError

from base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        try:
            entries = self.db.get("SELECT * FROM Entry LIMIT 5")
        except ProgrammingError:
            self.redirect("/install")
            return
        self.render('index.html', entries = entries)
