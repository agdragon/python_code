#!/usr/bin/env python
#coding=utf-8

'''
#-- 对象引用对象，容器对象中包含的并不是元素对象本身，是指向各个元素对象的引用。
#-- 对象引用对象，是Python最基本的构成方式。即使是a = 1这一赋值方式，实际上是让字典的一个键值"a"的元素引用整数对象1。
	该字典对象用于记录所有的全局引用。该字典引用了整数对象1。我们可以通过内置函数globals()来查看该字典。
'''

class from_obj(object):
    def __init__(self, to_obj):
        self.to_obj = to_obj

b = [1,2,3]
a = from_obj(b)
print(id(a.to_obj))
print(id(b))

c = 1

'''
#-- 结果:
	39899008
	39899008
'''

print locals()
print globals()