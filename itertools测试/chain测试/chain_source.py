#! /usr/bin/env python
#coding=utf-8

'''
	# chain源码实现
'''

def chain(*iterables):
	for it in iterables:
		for item in it:
			yield item

def main():
	for i in chain([1, 2, 3], ['a', 'b', 'c']):
		print i

if __name__ == '__main__':
	main()