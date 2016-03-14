#!/usr/bin/python
#coding=utf-8

'''
#-- callback要抛出异常，尝试去捕获异常。
'''

import tornado.ioloop
IL = tornado.ioloop.IOLoop.instance()

def callback():
    raise Exception, 'Exception in callback...'

def func():
    IL.add_callback(lambda: out(callback))

def out(func):
    try:
    	print "func called..."
        func()
    except Exception, e:
        print e

func()
IL.start()

'''
#-- 结果:
	
	func called...
    Exception in callback...

'''

'''
#-- 结论:
	
	捕获到异常。

'''