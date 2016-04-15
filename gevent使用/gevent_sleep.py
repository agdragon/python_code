#!/usr/bin/python
#coding=utf-8

import gevent

def test(id):
    print('Test %s is running...' % id)
    gevent.sleep(0)
    print('Test %s is done!' % id)

gevent.joinall([gevent.spawn(test, i) for i in range(2)])