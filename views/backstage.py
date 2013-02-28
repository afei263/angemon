# -*- coding: utf-8 -*-

import logging
import hashlib

import tornado.web

from views.base import BaseHandler
from models.user import UserHelper
from models.entry import Entry
from models.entry import EntryHelper

class SigninHandler(BaseHandler, UserHelper):
    def get(self):
        self.render("backstage.signin.html")
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        error = []
        if not 3 < len(username) < 20:
            error.append("Username is too long or too short!")
        user = self.select_user_by_username(username.lower())
        hashed_password = hashlib.sha1(password).hexdigest()
        logging.info(username)
        logging.info(password)
        logging.info(hashed_password)
        logging.info(user)
        if not user or user.password != hashed_password:
            error.append("Wrong Username and password combination.")
        if error:
            logging.info(error)
            self.render("backstage.signin.html")
            return
        auth = user.create_auth()
        self.db.add(auth)
        self.db.commit()
        self.set_secure_cookie("token", auth.secret)
        self.redirect("/")

class ComposeHandler(BaseHandler, EntryHelper):
    @tornado.web.authenticated
    def get(self):
        pid = self.get_argument("pid", None)
        entry = None
        if pid:
            try:
                pid = int(pid)
            except ValueError:
                pid = None
        if pid:
            entry = self.select_entry_by_id(pid)
        logging.info(entry)
        self.render("compose.html")
    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title", "")
        content = self.get_argument("content", "")
        slug = self.get_argument("slug", "")
        draft = self.get_argument("draft", None)
        logging.info("draft: %s", draft)
        if draft and draft.lower() == "on":
            draft = True
        else:
            draft = False
        error = []
        if not title or not content:
            error.append("Title or content is required.")
        if error:
            self.render("compose.html", entry = { "title" : title, \
                                                  "content" : content, \
                                                  "slug" : slug, \
                                                  "draft" : draft})
            return
        entry = Entry(title, content, self.current_user, slug, draft)
        self.db.add(entry)
        self.db.commit()
        self.redirect('/%s/' % entry.slug)
