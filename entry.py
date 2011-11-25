# -*- coding: utf-8 -*-

from markdown import markdown

import tornado.web

from base import BaseHandler

class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('newentry.html', title = None, content = None, error = 0)
    @tornado.web.authenticated
    def post(self):
        title = self.get_argument('title', default = "No Title")
        content = self.get_argument('content', default = None)
        if not content:
            self.render('newentry.html', title = title, content = content, error = 1)
            return
        self.db.execute("INSERT INTO Entry(Title, Content, Author_id, PublishTime) \
                         VALUES (%s, %s, %s, UTC_TIMESTAMP())", \
                         title, content, self.current_user.id)
        self.redirect("/backstage")


class EntryHandler(BaseHandler):
    def get(self, eid):
        entry = self.db.get("SELECT * FROM Entry WHERE id = %s", eid)
        if not entry:
            raise tornado.web.HTTPError(404)
        author = self.db.get("SELECT * FROM User WHERE id = %s", entry.Author_id)
        self.render("entry.html", entry = entry, content = markdown(entry.Content), author = author)

class EditEntryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, eid):
        entry = self.db.get("SELECT * FROM Entry WHERE id = %s", eid)
        if not entry:
            raise tornado.web.HTTPError(404)
        self.render("edit.html", entry = entry)
    def post(self, eid):
        entry = self.db.get("SELECT * FROM Entry WHERE id = %s", eid)
        if not entry:
            raise tornado.web.HTTPError(404)
        title = self.get_argument('title', default = "No Title")
        content = self.get_argument('content', default = None)
        self.db.execute("UPDATE Entry SET Title = %s, Content = %s, PublishTime = UTC_TIMESTAMP() WHERE id = %s", \
                        title, content, eid)
        self.redirect("/entry/" + str(eid) + "/edit")
