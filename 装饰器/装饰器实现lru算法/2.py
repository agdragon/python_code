#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def log(prefix):
    root = []
    def log_decorator(f):
        def wrapper(*args, **kw):
            print '[%s] %s()...' % (prefix, f.__name__)
            root.append(f.__name__)
            print root
            print "\n"
            return f(*args, **kw)
        return wrapper
    return log_decorator
 
@log('DEBUG')   #此处log第一次被调用。
def test():
    pass

@log('DEBUG')   #此处log被二次调用。
def test_1():
    pass

test()
test_1()
test()
test()
