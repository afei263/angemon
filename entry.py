# -*- coding: utf-8 -*-

import tornado.web

from base import BaseHandler

class NewEntryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        self.render('newentry.html', user = user)
