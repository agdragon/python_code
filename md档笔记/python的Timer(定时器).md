# python的Timer(定时器)

标签（空格分隔）： python

---

Timer:  隔一定时间调用一个函数,如果想实现每隔一段时间就调用一个函数的话，就要在Timer调用的函数中，再次设置Timer。Timer是Thread的一个派生类
代码如下:
```
import threading
import time

def hello(name):
    print "hello %s\n" % name

    global timer
    timer = threading.Timer(2.0, hello, ["Hawk"])
    timer.start()

if __name__ == "__main__":
    timer = threading.Timer(2.0, hello, ["Hawk"])
    timer.start()
```




