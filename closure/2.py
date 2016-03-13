#!/usr/bin/python
#coding=utf-8

def test():
	x = [1, 2]
	print hex(id(x))

	def a():
		x.append(3)
		print hex(id(x))
	
	def b():
		print hex(id(x)), x
	
	return a, b

a, b = test()
a()
b()
print "**********************"
print a.func_closure
print b.func_closure

print "**********************"
print a
print b