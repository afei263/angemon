# -*- coding: utf-8 -*-
# Author: Zeray Rice <fanzeyi1994@gmail.com>

import os
import sys

import tornado.web
import tornado.ioloop
import tornado.database
import tornado.httpserver

from db import ConnectDB
from base import BaseHandler
from main import IndexHandler
from admin import SigninHandler
from admin import SignoutHandler
from admin import InstallHandler
from admin import BackstageHandler
from entry import ComposeHandler
from entry import EntryHandler
from entry import EditEntryHandler
from entry import RemoveEntryHandler
from entry import FeedHandler
from config import site_config
from config import mysql_config

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler), 
            (r'/signin', SigninHandler), 
            (r'/signout', SignoutHandler),
            (r'/install', InstallHandler),  
            (r'/backstage', BackstageHandler),
            (r'/compose', ComposeHandler),
            (r'/entry/([^/]+)', EntryHandler), 
            (r'/entry/([^/]+)/edit', EditEntryHandler), 
            (r'/entry/([^/]+)/remove', RemoveEntryHandler), 
            (r'/feed', FeedHandler), 
        ]
        settings = {
            'site_title' : site_config["site_title"], 
            'login_url' : '/signin', 
            'template_path' : os.path.join(os.path.dirname(__file__), 'tpl'), 
            'static_path' : os.path.join(os.path.dirname(__file__), "static"),
            'xsrf_cookies' : True, 
            'cookie_secret' : '3295bfab668c4ad48dad43f890402905',
            'google_analytics' : site_config["google_analytics"], 
            'feed_url' : site_config["feed_url"], 
        }
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session = ConnectDB()

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(int(sys.argv[-1]))
    tornado.ioloop.IOLoop.instance().start()
