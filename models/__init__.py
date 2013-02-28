# -*- coding: utf-8 -*-

from models.user import *
from models.auth import *
from models.entry import *
from models.base import Base

def init_db(engine):
    Base.metadata.create_all(bind = engine)
