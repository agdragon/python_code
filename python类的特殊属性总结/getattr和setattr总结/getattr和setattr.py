#!/usr/bin/env python
#coding=utf-8

#Dict object, 继承自dict类，实现了a.b的访问字典元素的方式
class Dict(dict):
    '''
    一个简单的字典类，继承自dict，实现了a.b的访问字典元素的方式
    操作实例：
    >>> d1 = Dict();
    >>> d1['x'] = 100
    >>> d1.x
    100

    >>> d1.y = 200
    >>> d1['y']
    200

    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'

    >>>d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'


    >>> d3 = Dict(('a','b','c'), (1,2,3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    '''
    

    '''
    构造函数
    @param1 实例self
    @param2 元组
    @param3 元组
    @param4 字典
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k,w in zip(names, values):
            self[k] = w


    '''
    这里使用定制类来实现类a.b风格的调用方式。
    当调用不存在的属性时，比如score，Python解释器会试图调用__getattr__(self, 'score')来尝试获得属性，这样，我们就有机会返回score的值
    '''
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    '''
    这里使用定制类来实现类a.b=5风格的调用方式。
    当赋值给不存在的属性时，比如score，Python解释器会试图调用__setattr__(self, 'score')来尝试去赋值给属性，这样，我们就有机会给scope属性赋值
    '''
    def __setattr__(self, key, value):
        self[key] = value

d3 = Dict(('a','b','c'), (1,2,3))
print d3.a
print d3.b
d3.a = 5
print d3.a