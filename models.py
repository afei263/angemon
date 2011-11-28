# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base

from config import mysql_config

ConnectString = "mysql://%s:%s@%s/%s?charset=utf8" % (mysql_config['mysql_user'], 
                                                      mysql_config['mysql_password'], 
                                                      mysql_config['mysql_host'], 
                                                      mysql_config['mysql_database'])

engine = create_engine(ConnectString, encoding='utf8', convert_unicode=True)
metadata = MetaData()
metadata.create_all(engine) 
Base = declarative_base()

Entry_Table = Table('Entry', metadata, 
                    Column('id', Integer, primary_key = True), 
                    Column('Title', String(100)), 
                    Column('Content', TEXT(4294967295)), 
                    Column('Markdown', TEXT(4294967295)), 
                    Column('Author_id', Integer, ForeignKey('User.id')), 
                    Column('PublishTime', DATETIME), 
                    Column('UpdateTime', DATETIME), 
                    mysql_charset = 'utf8')

User_Table = Table('User', metadata, 
                   Column('id', Integer, primary_key = True), 
                   Column('Username', String(40)), 
                   Column('Auth', String(40)), 
                   Column('Nickname', String(40)), 
                   mysql_charset = 'utf8')

Site_Table = Table('Site', metadata, 
                   Column('id', Integer, primary_key = True), 
                   Column('Analytics', String(40)), 
                   Column('Feed', String(300)), 
                   mysql_charset = 'utf8')

metadata.create_all(engine)

class Entry(Base):
    __tablename__ = 'Entry'
    id = Column(Integer, primary_key = True)
    Title = Column(String)
    Content = Column(TEXT)
    Markdown = Column(TEXT)
    Author_id = Column(Integer, ForeignKey('User.id'))
    Author = relation('User', lazy = 'immediate', order_by = 'User.id')
    PublishTime = Column(DATETIME)
    UpdateTime = Column(DATETIME)

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key = True)
    Username = Column(String)
    Auth = Column(String)
    Nickname = Column(String)

class Site(Base):
    __tablename__ = 'Site'
    id = Column(Integer, primary_key = True)
    Analytics = Column(String)
    Feed = Column(String)
