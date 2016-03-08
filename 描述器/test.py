#!/usr/bin/python
# -*- coding: utf-8 -*-

class RevealAccess(object):
    """A data descriptor that sets and returns values
    normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, instance, owner):
        '''
        instance指的是temp，而owner则是Temperature。
        '''
        print('Retrieving', self.name)
        return self.val

    def __set__(self, instance, val):
        print('Updating', self.name)
        self.val = val

class Temperature(object):
    x = RevealAccess(10, 'xds')
    y = 5
    def __init__(self, y):
        # self.x = x
        self.y = y

temp = Temperature(100)
a = Temperature.x
print a

