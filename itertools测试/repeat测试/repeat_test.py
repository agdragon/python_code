#! /usr/bin/env python
#coding=utf-8

from itertools import repeat

'''
	# 创建一个迭代器，重复生成object，times（如果已提供）指定重复计数，如果未提供times，将无止尽返回该对象。
'''

def main():
	for i in repeat("over-and-over", 5):
		print i

if __name__ == '__main__':
	main()