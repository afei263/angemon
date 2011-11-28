# -*- coding: utf-8 -*-

import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    @property
    def session(self):
        return self.application.session
    def get_current_user(self):
        auth = self.get_secure_cookie("auth")
        if not auth:
            return None
        return self.db.get("SELECT * FROM User WHERE Auth = %s", auth)
