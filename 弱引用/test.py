#!/usr/bin/env python
#coding=utf-8

'''
python 弱引用的小实验
'''

import weakref
import gc

def my_callback(obj):
	print "回收了垃圾"

class NewObj(object):
    def my_method(self):
        print "called me "

obj = NewObj()
r = weakref.ref(obj, my_callback)
gc.collect()
print obj
print r()
obj.my_method()
r().my_method()

obj = 1

print r()

'''
<__main__.NewObj object at 0x01B94090>
<__main__.NewObj object at 0x01B94090>
called me 
called me 
回收了垃圾
None

说明了，当一开始分配的对象不存在引用时，就会回收刚刚的内存
'''