# -*- coding: utf-8 -*-

from models.base import Base

def init_db(engine):
    Base.metadata.create_all(bind=engine)
