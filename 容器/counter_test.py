#!/usr/bin/python
#coding=utf-8

from collections import Counter

a = [1,2,3,4,6,6,6]
print Counter(a)

print "\n"

colours = (
    ('Yasoob', 'Yellow'),
    ('Ali', 'Blue'),
    ('Arham', 'Green'),
    ('Ali', 'Black'),
    ('Yasoob', 'Red'),
    ('Ahmed', 'Silver'),
)

tmpList = [name for name, colour in colours]
print Counter(tmpList)