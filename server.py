# -*- coding: utf-8 -*-
# Author: Zeray Rice <fanzeyi1994@gmail.com>

import os
import sys

import tornado.web
import tornado.ioloop
import tornado.database
import tornado.httpserver
from tornado.options import define
from tornado.options import options

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
from config import mysql_config

define("mysql_host", default = mysql_config['mysql_host'])
define("mysql_database", default = mysql_config['mysql_database'])
define("mysql_user", default = mysql_config['mysql_user'])
define("mysql_password", default = mysql_config['mysql_password'])

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
            'site_title' : u'Angemon', 
            'login_url' : '/signin', 
            'template_path' : os.path.join(os.path.dirname(__file__), 'tpl'), 
            'static_path' : os.path.join(os.path.dirname(__file__), "static"),
            'xsrf_cookies' : True, 
            'cookie_secret' : '3295bfab668c4ad48dad43f890402905',
        }
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = tornado.database.Connection(
                  host=options.mysql_host, database=options.mysql_database,
                  user=options.mysql_user, password=options.mysql_password)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(int(sys.argv[-1]))
    tornado.ioloop.IOLoop.instance().start()
