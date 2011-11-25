# -*- coding: utf-8 -*-

from base import BaseHandler

class SigninHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if user:
            self.redirect('/')
        self.render('signin.html')
