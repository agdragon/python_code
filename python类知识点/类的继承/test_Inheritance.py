#! /usr/bin/env python
#coding=utf-8

'''
类的继承，利用super函数实现在子类中调用父类相关的函数

'''

class A(object):
	"""docstring for A"""
	def __init__(self):
		print "A class"

	def test(self):
		print "A class: test function"

	def test_1(self):
		print "A class: test_1 function"


class B(A):
	"""docstring for B"""
	def __init__(self):
		super(B,self).__init__()
		print ("B class")
	def  test(self):
		print "B class: test function"
		super(B, self).test_1()
		

# a = A()
# a.test()

b = B()
b.test()
b.test_1()

