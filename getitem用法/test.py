#!/usr/bin/env python
#coding=utf-8

'''
Python类的__getitem__和__setitem__特殊方法
'''

from threading import local


class testsetandget:
	def __init__(self):
		self._caches = local()

	def __getitem__(self, key): 
		try:
			return self._caches.caches[key]; 
		except AttributeError:
			self._caches.caches = {}
		except KeyError:
			pass

		

		return 4
        

    # def __setitem__(self, key, value):  
    #     self.kk[key] = value;

a = testsetandget()
# a['first'] = 1
print a['first']



# a.__setitem__('second', 2)
# print a.__getitem__('second')
# print a['second']