#! /usr/bin/env python
#coding=utf-8

class A(object):
    def __init__(self, arg = None):
        super(A, self).__init__()
        self.arg = arg

a = A(arg = 1)
print a.arg
        

def func(b = []):
    b.append(1)
    return b

print func()
print func()
print func()


def funcC(a, b=0):
    print a
    print b

funcC(b = 10, a = 200)