#!/usr/bin/env python
#coding=utf-8

import gc

'''

#--- 自动启动垃圾回收的时机：
	当Python运行时,会记录其中分配对象(object allocation)和取消分配对象(object deallocation)的次数。
	当两者的差值高于某个阈值时，垃圾回收才会启动。

	当然我们也可以手动启动垃圾回收，即使用gc.collect()。

'''

print (gc.get_threshold())

'''
#--- 结果分析:
	
	(700, 10, 10)

	后面的两个10是与分代回收相关的阈值。700即是垃圾回收启动的阈值。
'''

'''
#--- 分代回收:
	
	Python将所有的对象分为0，1，2三代。所有的新建对象都是0代对象。当某一代对象经历过垃圾回收，依然存活，那么它就被归入下一代对象。
	垃圾回收启动时，一定会扫描所有的0代对象。如果0代经过一定次数垃圾回收，那么就启动对0代和1代的扫描清理。
	当1代也经历了一定次数的垃圾回收后，那么会启动对0，1，2，即对所有对象进行扫描。

	这两个次数即上面get_threshold()返回的(700, 10, 10)返回的两个10。也就是说，每10次0代垃圾回收，会配合1次1代的垃圾回收；
	而每10次1代的垃圾回收，才会有1次的2代垃圾回收。


	同样可以用set_threshold()来调整，比如对2代对象进行更频繁的扫描。
	import gc
	gc.set_threshold(700, 10, 5)

'''
