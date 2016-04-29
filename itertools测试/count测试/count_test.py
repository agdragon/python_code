#! /usr/bin/env python
#coding=utf-8

from itertools import count

'''
	# 创建一个迭代器，生成从n开始的连续整数，如果忽略n，则从0开始计算(注意：此迭代器不支持长整数)
	# 如果超出了sys.maxint，计数器将溢出并继续从-sys.maxint-1开始计算。
'''

def main():
	for i in count(10,10):
		print i

if __name__ == '__main__':
	main()