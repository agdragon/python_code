#!/usr/bin/python
#coding=utf-8

import gevent

def foo():
	print ("Running in foo")
	gevent.sleep(0)
	print ("Running in foo again")

def bar():
	print ("Running in bar")
	gevent.sleep(0)
	print ("Running in bar again")

if __name__ == '__main__':
	gevent.joinall([
			gevent.spawn(foo),
			gevent.spawn(bar)
		])