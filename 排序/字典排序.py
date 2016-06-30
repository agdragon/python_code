#!/usr/bin/env python
#coding=utf-8

import operator

x = {"a":87, "b":67, "c":908}

# 按key来排序:
tmp = sorted(x.items(), key = operator.itemgetter(0))
print tmp


# 按value来排序:
tmp = sorted(x.items(), key = operator.itemgetter(1))
print tmp