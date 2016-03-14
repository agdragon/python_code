#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @date     2016-3-14
# @desc		读写锁的用法
#


import threading
from RWLock import RWLock

_caches = {}
_locks = {}



def write_data(cache, lock):
    with lock.writer():
    	print "write_data..."

def read_data(cache, lock):
    pass


def main(name):
	cache = _caches.setdefault(name, {})
	lock = _locks.setdefault(name, RWLock())

	threads = []
	t1 = threading.Thread(target=write_data, args=(cache, lock,))
	threads.append(t1)
	
	t2 = threading.Thread(target=read_data, args=(cache, lock,))
	threads.append(t2)

	for t in threads:
		# t.setDaemon(True)
		t.start()



if __name__ == '__main__':
	main("xds")