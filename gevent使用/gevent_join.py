#!/usr/bin/python
#coding=utf-8

import gevent

def test1(id):
    print(id)
    gevent.sleep(0)
    print(id, 'is done!')

t = gevent.spawn(test1, 't')
t1 = gevent.spawn(test1, 't1')
t.join()