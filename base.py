# -*- coding: utf-8 -*-

import tornado.web

from models import User

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
        query = self.session.query(User).filter_by(Auth = auth)
        if query.count() == 0:
            return None
        return query.one()
