#!/usr/bin/python
#coding=utf-8

'''
@functools.wraps(f)主要作用是让装饰后的函数能继续把原函数当爹
'''

import functools

def deco(f):
    @functools.wraps(f)
    def hello(*args, **kwargs):
        print(f.__name__) # print `test`
    return hello

@deco
def test():
    return 1 + 1

test()

print(test.__name__) # print `hello`