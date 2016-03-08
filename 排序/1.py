#!/usr/bin/env python
#coding=utf-8

import operator

x = {"a":87, "b":67, "c":908}
y = [1,453,56,34,5345]
tmp = sorted(x.items(), key = operator.itemgetter(1))
print tmp

print y.sort()
print y