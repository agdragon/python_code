#!/usr/bin/env python
#coding=utf-8
from ctypes import *

class PyObject(Structure):
    _fields_ = [("refcnt", c_size_t),
                ("typeid", c_void_p)]

a = "this is a string"
obj_a = PyObject.from_address(id(a))	#通过 id(a) 可以获得对象 a 的内存地址，而 PyObject.from_address()可以将指定的内存地址的内容转换为一个 PyObject 对象

print obj_a.refcnt #查看对象 a 的引用次数

b = [a]*10	#接下来创建一个列表，此列表中的每个元素都是对象 a，因此此列表应用了它 10 次，所以引用次数变为了 11
print obj_a.refcnt

print obj_a.typeid #查看对象 a 的类型对象的地址，它和 id(type(a)) 相同，而由于对象a的类型为str，因此也就是 id(str)

print id(type(a))
print id(str)