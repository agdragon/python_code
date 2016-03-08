#!/usr/bin/python
#coding=utf-8

"""
	类做装饰器，需要注意的是要在定义：__call__，同时需要返回参数arg，此arg就是被装饰的类
	该装饰器经常用到需要统计所有类的一些信息
"""

class A():
	global_list = []
	def __init__(self,arg):
		print "A............."
		self.arg = arg

	def __call__(self,arg):
		# print "*" * 10
		# print arg
		# print "*" * 10

		self.global_list.append((self.arg, arg))

		return arg

	@classmethod
    def get_global_list(cls):
        return cls.global_list


@A("xds")
class B():
	def __init__(self):
		print "B.............."

		
if __name__ == '__main__':
	b = B()	
	# a = A()
	print A.get_global_list()
