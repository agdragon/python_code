#!/usr/bin/python
# coding=utf-8

'''
1:创建函数并将其作为单个进程
2:os.getpid()获取当前进程的id
'''

import multiprocessing
import time
import os


def worker(interval):
    n = 5
    while n > 0:
        print("The time is {0}".format(time.ctime()))
        time.sleep(interval)
        n -= 1

if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.start()
    print "p.pid:", p.pid
    print "p.name:", p.name
    print "p.is_alive:", p.is_alive()
    print os.getpid()
    p.join()