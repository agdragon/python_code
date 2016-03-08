#!/usr/bin/env python
#coding=utf-8

#用list去执行生成器，同时得到生成器的结果

def test_1():
	print "aaaaaaaaaaaaaa"
	yield 1
	print "bbbbbbbbbbbbbb"
	yield 2
	print "cccccccccccccc"
	yield 3
	print "dddddddddddddd"
	yield 4

if __name__ == "__main__":
	m = test_1()
	# print type(m)
	# print m
	# b = list(m)
	# print b

	for i in m:
		print i
		print "\n"

#测试结果:
'''
<type 'generator'>
<generator object test_1 at 0x01B84648>
aaaaaaaaaaaaaa
bbbbbbbbbbbbbb
cccccccccccccc
dddddddddddddd
# [1, 2, 3, 4]


for i in m:
	print i'''