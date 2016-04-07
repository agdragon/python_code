#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lru_cache import lru_cache
import time

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

def main():
	tmp = [fib(n) for n in range(16)]
	print tmp
	print "\n"
	print fib.cache_info()


@lru_cache(maxsize=50, typed=True)
def test_1(m, n):
	time.sleep(1)
	return m*n

if __name__ == '__main__':
	for i in xrange(0,100):
		if i % 2 == 0:
			print test_1(20,23)
			print test_1.cache_info()
		else:
			print test_1(20,23.4)
			print test_1.cache_info()
