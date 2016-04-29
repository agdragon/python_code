#! /usr/bin/env python
#coding=utf-8


'''
	# 实现count的源码
'''

def count(start = 0, step = 1):
	n = start
	while True:
		yield n
		n = n + step

def main():
	for i in count(10,10):
		print i

if __name__ == '__main__':
	main()