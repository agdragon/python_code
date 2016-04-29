#! /usr/bin/env python
#coding=utf-8

from itertools import cycle

'''
	# 创建一个迭代器，对iterable中的元素反复执行循环操作，内部会生成iterable中的元素的一个副本，此副本用于返回循环中的重复项。
'''

def main():
	i = 0
	for item in cycle(['a', 'b', 'c']):
		i += 1
		if i == 10:
			break
		print (i, item)

if __name__ == '__main__':
	main()