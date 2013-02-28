# -*- coding: utf-8 -*-

import tornado.web

from models.auth import Auth

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    @property
    def jinja2(self):
        return self.application.jinja2
    def render(self, name, **kwargs):
        if "self" in kwargs.keys():
            kwargs.pop("self")
        template = self.jinja2.get_template(name)
        rendered_page = template.render(page = self, user = self.current_user, **kwargs)
        self.write(rendered_page)
        self.db.close()
        self.finish()
    def get_current_user(self):
        token = self.get_secure_cookie('token')
        if not token:
            return None
        query = self.db.query(Auth).filter_by(secret = token)
        if query.count() == 0:
            return None
        auth = query.one()
        if auth.is_valid():
            auth.update_time(self.db)
            return auth.user
        return None
