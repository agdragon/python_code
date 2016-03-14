#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @date     2016-3-14
# @desc		创建线程
#

import threading


def write_data(cache, lock):
	print cache + ":" + lock

def read_data(cache):
    print cache


def main(name):
	threads = []
	t1 = threading.Thread(target=write_data, args=("cache", "lock",))
	threads.append(t1)
	
	t2 = threading.Thread(target=read_data, args=("cache",))
	threads.append(t2)

	for t in threads:
		# t.setDaemon(True)
		t.start()



if __name__ == '__main__':
	main("xds")