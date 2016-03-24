#!/usr/bin/env python
#coding=utf-8


class A():
	m = 1
	def __init__(self, arg):
		self.m = arg
		

print A.m

a = A(10)
print a.m
print A.m
