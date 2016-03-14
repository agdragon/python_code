#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
#
# @author   xubigshu@gmail.com
# @date     2016-3-14
# @desc		Semaphore的用法
			Semaphore管理一个内置的计数器，
			每当调用acquire()时内置计数器-1；
			调用release() 时内置计数器+1；
			计数器不能小于0；当计数器为0时，acquire()将阻塞线程直到其他线程调用release()。
#
'''

import threading
import time

semaphore = threading.Semaphore(2)
 
def func():
	if semaphore.acquire():
		print (threading.currentThread().getName() + ' get semaphore')
		
		time.sleep(1)

		semaphore.release()
		
		print (threading.currentThread().getName() + ' release semaphore')

for i in range(4):
	t1 = threading.Thread(target=func)
	t1.start()