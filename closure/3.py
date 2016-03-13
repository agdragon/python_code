#!/usr/bin/python
#coding=utf-8

def foo():  
	# a = 1  
	a = [1]  
	def bar():  
		a[0] = a[0] +1  
		return a[0]  
		# print a
	return bar

tmp = foo()
print type(tmp)
print tmp()