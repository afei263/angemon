# -*- coding: utf-8 -*-

from views.index import IndexHandler
from views.entry import EntryHandler
from views.backstage import SigninHandler
from views.backstage import ComposeHandler

route = [
    (r'/', IndexHandler), 
    (r'/backstage/signin', SigninHandler), 
    (r'/backstage/compose', ComposeHandler), 
    (r'/(.*)', EntryHandler), 
]
