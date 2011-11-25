# -*- coding: utf-8 -*-

import hashlib

from base import BaseHandler

class InstallHandler(BaseHandler):
    def get(self):
        count = self.db.get("SELECT count(1) as count FROM User")
        if count['count'] != 0:
            raise tornado.web.HTTPError(404)

class SigninHandler(BaseHandler):
    def get(self):
        count = self.db.get("SELECT count(1) as count FROM User")
        if count['count'] == 0:
            self.redirect('/install')
        user = self.get_current_user()
        if user:
            self.redirect('/')
        self.render('signin.html', usr = None, error = 0)
    def post(self):
        user = self.get_current_user()
        if user:
            self.redirect('/')
        usr = self.get_argument("usr", default = None)
        pwd = self.get_argument("pwd", default = None)
        if not usr or not pwd:
            self.render('signin.html', usr = usr, error = 1)
            return
        auth = hashlib.sha1(str(usr) + str(pwd) + "angemon").hexdigest()
        query = self.db.get("SELECT * FROM User WHERE `Username` = %s AND `Auth` = %s", usr, auth)
        if not query:
            self.render('signin.html', usr = usr, error = 2)
            return
        self.set_secure_cookie('auth', auth)
        self.redirect('/')
