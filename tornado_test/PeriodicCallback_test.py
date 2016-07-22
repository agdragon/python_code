#! /usr/bin/env python
#coding=utf-8

from tornado.ioloop import PeriodicCallback

def test():
	print "aaaaaaaaaaaa"

PeriodicCallback(test, 1000).start()

'''
这样是不行的，必须要启动IOLoop才行，见test.py中的测试代码。
'''

'''
大概扫了一下源码，是就是递归调用add_timeout(deadline, callback)函数，每次在添加的callback中再次执行了add_timeout，所以实现了周期调用。
'''