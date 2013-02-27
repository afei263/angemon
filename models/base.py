# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import UnicodeText
from sqlalchemy.sql import func
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class baseModule(object):
    id = Column(Integer, primary_key = True)
    createTime = Column(DateTime, default = func.current_timestamp()) 
    updateTime = Column(DateTime, default = func.current_timestamp())
