#!/usr/bin/env python
#coding=utf-8

import tornado.ioloop
from tornado.gen import coroutine
from tornado.concurrent import Future

@coroutine
def asyn_sum(a, b):
    print("begin calculate:sum %d+%d"%(a,b))

    future = Future()
    future2 = Future()
    
    iol = tornado.ioloop.IOLoop.instance()

    def callback(a, b):
        print("calculating the sum of %d+%d:"%(a,b))
        future.set_result(a+b)

        iol.add_timeout(iol.time()+3,lambda f:f.set_result("xds test"),future2)
    print "aaaaaaaaaaaaaaaaaaaaaa"
    iol.add_timeout(iol.time()+3,callback, a, b)
    print "bbbbbbbbbbbbbbbbbbbbbb"

    # print "now time is :" + str(iol.time())
    result = yield future
    
    print "ccccccccccccccccccccc"

    f2Result = yield future2
    

def main():
    f =  asyn_sum(2,3)

    print "跳出了协程代码"

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()