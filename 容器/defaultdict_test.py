#!/usr/bin/python
#coding=utf-8

from collections import defaultdict

'''
# 	defaultdict(function_factory)构建的是一个类似dictionary的对象，
	其中keys的值，自行确定赋值，
	但是values的类型，是function_factory的类实例，而且具有默认值。
	比如default(int)则创建一个类似dictionary对象，里面任何的values都是int的实例，
	而且就算是一个不存在的key, d[key] 也有一个默认值，这个默认值是int()的默认值0.
'''


def test_1():
	colours = (
		('Yasoob', 'Yellow'),
		('Ali', 'Blue'),
		('Arham', 'Green'),
		('Ali', 'Black'),
		('Yasoob', 'Red'),
		('Ahmed', 'Silver'),
	)

	d = defaultdict(list)


	for name, colour in colours:
		d[name].append(colour)

	print(d)


def default_factory():
    return 'default value'

def test_2():
	d=defaultdict(default_factory,foo='bar',ok='ok')
	print 'd:',d
	print 'foo=',d['foo']
	print 'ok=',d['ok']
	print 'bar=',d['bar']

if __name__ == "__main__":
	# test_1()
	test_2()