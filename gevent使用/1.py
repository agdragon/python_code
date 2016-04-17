#!/usr/bin/python
#coding=utf-8

import gevent

def talk(msg):
    print(msg)

g1 = gevent.spawn(talk, 'bar')

print type(g1)

print getcurrent()

gevent.sleep(0)