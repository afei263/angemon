# -*- coding: utf-8 -*-

import tornado.web

from models.user import User

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
        query = self.db.query(User).filter_by(token = token)
        if query.count() == 0:
            return None
        return query.one()
