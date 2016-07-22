#!/usr/bin/python
#coding=utf-8

'''
#-- callback要抛出异常，但是不能捕获到。
'''

import tornado.ioloop
IL = tornado.ioloop.IOLoop.instance()


def callback():
    raise Exception, 'Exception in callback'

def func():
    IL.add_callback(callback)

def out():
    try:
    	print "func called..."
        func()
    except:
        print 'ok'

out()
IL.start()

'''
#-- 结果:
	
	func called...

'''

'''
#-- 结论:
	
	没能捕获到异常。

'''
