# -*- coding: utf-8 -*-

import hashlib

import tornado.web
from sqlalchemy import desc

from db import ConnectDB
from base import BaseHandler
from models import Site
from models import User
from models import Entry

class InstallHandler(BaseHandler):
    def get(self):
        site = self.session.query(Site)
        if site.count() != 0:
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
        user = User()
        user.Username = usr
        user.Auth = auth
        user.Nickname = nickname
        self.session.add(user)
        site = Site()
        self.session.add(site)
        self.session.commit()
        self.redirect('/signin')

class SigninHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect('/backstage')
            return 0
        self.render('signin.html', usr = None, error = 0)
    def post(self):
        if self.current_user:
            self.redirect('/')
        usr = self.get_argument("usr", default = None)
        pwd = self.get_argument("pwd", default = None)
        if not usr or not pwd:
            self.render('signin.html', usr = usr, error = 1)
            return
        auth = hashlib.sha1(str(usr) + str(pwd) + "angemon").hexdigest()
        query = self.session.query(User).filter_by(Auth = auth)
        if query.count() == 0:
            self.render('signin.html', usr = usr, error = 2)
            return
        self.set_secure_cookie('auth', auth)
        self.redirect('/')

class SignoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('auth')
        self.redirect('/')

class BackstageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        entries = self.session.query(Entry).order_by(desc('Entry.id')).all()
        self.render('backstage.html', entries = entries)
