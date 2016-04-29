#! /usr/bin/env python
#coding=utf-8


'''
	# 实现count的源码
'''

def  cycle(iterable):
	saved = []
	for item in iterable:
		yield item
		saved.append(item)
	while saved:
		for item in saved:
			yield item


def main():
	i = 0
	for item in cycle(["a","b","c","d"]):
		i += 1
		if i == 10:
			break

		print (i, item)

if __name__ == '__main__':
	main()