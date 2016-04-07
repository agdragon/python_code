#!/user/bin/python
# -*- coding: utf-8 -*-

'''
json实例化一个对象的方法
'''


import json
class User():
	def __init__(self):
		self.a = 1
		self.b = 2
		
user = User()
d = {}
d.update(user.__dict__)

print json.dumps(d)
