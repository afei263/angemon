# -*- coding: utf-8 -*-

import hashlib

import tornado.web

from base import BaseHandler

class InstallHandler(BaseHandler):
    def get(self):
        count = self.db.get("SELECT count(1) as count FROM User")
        if count['count'] != 0:
            raise tornado.web.HTTPError(404)
        self.render('install.html', usr = None, error = 0)
    def post(self):
        usr = self.get_argument("usr", default = None)
        pwd = self.get_argument("pwd", default = None)
        nickname = self.get_argument("nickname", default = "Angemon")
        if not usr or not pwd:
            self.render('install.html', usr = usr, error = 1)
        if len(usr) < 4 or len(pwd) < 5:
            self.render('install.html', usr = usr, error = 2)
        if len(usr) > 15 or len(pwd) > 15:
            self.render('install.html', usr = usr, error = 3)
        auth = hashlib.sha1(str(usr) + str(pwd) + "angemon").hexdigest()
        self.db.execute("INSERT INTO User(Username, Auth, Nickname) VALUES (%s, %s, %s)", \
                        usr, auth, nickname)
        self.redirect('/signin')

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
