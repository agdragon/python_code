#! /usr/bin/env python
#coding=utf-8

class A(object):
	def __init__(self, arg):
		super(A, self).__init__()
		self.arg = arg

a = A(1)
print A
print a.__class__

b = a.__class__(1)

print "******************"

c = A
print c
print type(c)
d = c(1)
