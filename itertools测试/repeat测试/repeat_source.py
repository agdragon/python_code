#! /usr/bin/env python
#coding=utf-8


'''
	# 实现repeat的源码
'''

def repeat(object, times=None):
	if times is None:
		while True:
			yield object
	else:
		for i in xrange(times):
			yield object

def main():
	for i in repeat("over-and-over", 5):
		print i

if __name__ == '__main__':
	main()