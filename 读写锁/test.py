#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @date     2016-3-14
# @desc		读写锁的用法
#


import threading
import time
from RWLock import RWLock

_caches = {}
_locks = {}

name = "data"

cache = _caches.setdefault(name, {})
lock = _locks.setdefault(name, RWLock())


def write_data(key, data):
	with lock.writer():
		cache[key] = data

def read_data(key):
	with lock.reader():
		print cache[key]
		print cache

def main():
	key = "key"
	data = {
		"a":1
	}

	threads = []
	t1 = threading.Thread(target=write_data, args=(key, data,))
	threads.append(t1)
	
	t2 = threading.Thread(target=read_data, args=(key,))
	threads.append(t2)

	for t in threads:
		t.start()



if __name__ == '__main__':
	main()