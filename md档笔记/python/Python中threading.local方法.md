#Python中threading.local方法

###概述:
`threading.local()`这个方法的特点用来保存一个全局变量，但是这个全局变量只有在当前线程才能访问


##**内容**

* 目录：

	* [代码](#user-content-代码)
 	* [结果](#user-content-结果)
 	* [分析](#user-content-分析)
 	* [结论](#user-content-结论)

<br>


* ####代码：
```
#coding=utf-8
import threading
# 创建全局ThreadLocal对象:
localVal = threading.local()
localVal.val = "Main-Thread"
def process_student():
    print '%s (in %s)' % (localVal.val, threading.current_thread().name)
def process_thread(name):
    #赋值
    localVal.val = name
    process_student()
t1 = threading.Thread(target= process_thread, args=('One',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Two',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
print localVal.val
```


* ####结果：
```
打印结果：

One (in Thread-A)
Two (in Thread-B)
Main-Thread
```


* ####分析：
`threading.local()`这个方法的特点用来保存一个全局变量，但是这个全局变量只有在当前线程才能访问，

localVal.val = name这条语句可以储存一个变量到当前线程，如果在另外一个线程里面再次对`localVal.val`进行赋值，
那么会在另外一个线程单独创建内存空间来存储，也就是说在不同的线程里面赋值 不会覆盖之前的值，因为每个

线程里面都有一个单独的空间来保存这个数据,而且这个数据是隔离的，其他线程无法访问


这个东西可以用在那些地方呢，比如下载，现在都是多线程下载了，就像酷狗那样，可以同时下载很多首歌曲，那么

就可以利用这个方法来保存每个下载线程的数据，比如下载进度，下载速度之类的



* ####结论：
所以  如果你在开发多线程应用的时候  需要每个线程保存一个单独的数据供当前线程操作，可以考虑使用这个方法，简单有效

其实这样的功能还有很多种方法可以实现，比如我们在主线程实例化一个`dict`对象，然后用线程的名字作为key，因为线程之间可以共享数据，

所以也可以实现相同功能，并且灵活性更多，不过代码就没那么优雅简洁了



