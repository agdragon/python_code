#!/usr/bin/python   
#coding=utf-8

'''
# 字典树
'''

class Node:
	"""
	# 字典树的每个节点
	"""
	def __init__(self):
		self.data = data
		self.children = {}

class TireTree:
	"""
	# 字典树的结构
	"""
	def __init__(self):
		self.root = Node()	#字典树的根节点里面不会存值

	def insert(self, value):
		node = self.root
		for char in value:
			if char not in node.children:
				child = Node()
				node.children[char] = children	#将字母当做子节点的key存入children字典中
				node = child
			else:
				node = node.children[char]
if __name__ == '__main__':
	tireTree = TireTree()	#创建一颗字典树
		
			 
