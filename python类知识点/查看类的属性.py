#!/usr/bin/python
# -*- coding: utf-8 -*-

class A(object):
	"""docstring for A"""
	def __init__(self, arg):
		super(A, self).__init__()
		self.arg = arg

print dir(A)
