# -*- coding: utf-8 -*-

import datetime

import tornado.web
from markdown import markdown as md
from sqlalchemy import desc

from base import BaseHandler
from models import Entry

def ApplyOption(option, entry):
    if option == "NO_FEED":
        entry.NoFeed = True
        return
    return

def CleanOption(entry):
    entry.NoFeed = False

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
        lines = content.splitlines()
        markdown = md(content)
        entry = Entry()
        if lines[0][0] == '@':
            options = lines[0][1:].split(",")
            for option in options:
                ApplyOption(option, entry)
            markdown = md("\n".join(lines[1:]))
        entry.Title = title
        entry.Content = content
        entry.Markdown = markdown
        entry.Author_id = self.current_user.id
        entry.PublishTime = datetime.datetime.now()
        entry.UpdateTime = datetime.datetime.now()
        self.session.add(entry)
        self.session.commit()
        self.redirect("/backstage")


class EntryHandler(BaseHandler):
    def get(self, eid):
        entry = self.session.query(Entry).get(eid)
        if not entry:
            raise tornado.web.HTTPError(404)
        self.render("entry.html", entry = entry)

class EditEntryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, eid):
        entry = self.session.query(Entry).get(eid)
        if not entry:
            raise tornado.web.HTTPError(404)
        self.render("edit.html", entry = entry)
    @tornado.web.authenticated
    def post(self, eid):
        entry = self.session.query(Entry).get(eid)
        if not entry:
            raise tornado.web.HTTPError(404)
        title = self.get_argument('title', default = "No Title")
        content = self.get_argument('content', default = None)
        lines = content.splitlines()
        markdown = md(content)
        CleanOption(entry)
        if lines[0][0] == '@':
            options = lines[0][1:].split(",")
            for option in options:
                ApplyOption(option, entry)
            markdown = md("\n".join(lines[1:]))
        entry.Title = title
        entry.Content = content
        entry.Markdown = markdown
        entry.UpdateTime = datetime.datetime.now()
        self.redirect("/entry/" + str(eid))

class RemoveEntryHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, eid):
        entry = self.session.query(Entry).get(eid)
        if not entry:
            raise tornado.web.HTTPError(404)
        self.render("remove.html", entry = entry)
    @tornado.web.authenticated
    def post(self, eid):
        entry = self.session.query(Entry).get(eid)
        self.session.delete(entry)
        self.session.commit()
        self.redirect("/")

class FeedHandler(BaseHandler):
    def get(self):
        entries = self.session.query(Entry) \
                              .filter_by(NoFeed = False) \
                              .order_by(desc('Entry.id')) \
                              .limit(10) \
                              .all()
        self.set_header("Content-Type", "application/atom+xml; charset=utf-8")
        self.render("feed.xml", entries = entries)
