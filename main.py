# -*- coding: utf-8 -*-

import os
import sys
import logging
from jinja2 import Environment
from jinja2 import FileSystemLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define
from tornado.options import options

import models
from route import route
from config import site_config

tornado.options.parse_command_line()

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'site_title' : site_config["site_title"], 
            'login_url' : '/signin', 
            'template_path' : os.path.join(os.path.dirname(__file__), 'template'), 
            'static_path' : os.path.join(os.path.dirname(__file__), "static"),
            'xsrf_cookies' : True, 
            'cookie_secret' : '3295bfab668c4ad48dad43f890402905',
            'google_analytics' : site_config["google_analytics"], 
            'feed_url' : site_config["feed_url"]
        }
        settings.update(site_config)
        tornado.web.Application.__init__(self, route, **settings)
        # i18n 
        # tornado.locale.load_gettext_translations(self.settings['i18n_path'], "stormwind")
        # jinja2
        jinja_env = Environment(loader = FileSystemLoader(self.settings['template_path']))
        self.jinja2 = jinja_env
        # SQLAlchemy
        engine = create_engine(self.settings['db_path'], convert_unicode = True)
        models.init_db(engine)
        self.db = scoped_session(sessionmaker(bind = engine))

if __name__ == '__main__':
    try:
        port = int(sys.argv[-1])
    except ValueError:
        port = 8080
    logging.info("Starting tornado listen to %d" % port)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
