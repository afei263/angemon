# -*- coding: utf-8 -*-

import functools

from sqlalchemy.orm.exc import NoResultFound

def protect_one(method):
    '''Protect .one() method dont raise exception'''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            retval = method(self, *args, **kwargs)
        except NoResultFound:
            return None
        return retval
    return wrapper

def modify(method):
    '''modified the data from database'''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        retval = method(self, *args, **kwargs)
        self.db.add(retval)
        self.db.commit()
        return retval
    return wrapper
