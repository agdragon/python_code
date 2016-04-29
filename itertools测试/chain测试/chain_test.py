#! /usr/bin/env python
#coding=utf-8

from itertools import chain

'''
	# 实现chain的源码
'''

def main():
	for i in chain([1, 2, 3], ['a', 'b', 'c']):
		print i

if __name__ == '__main__':
	main()