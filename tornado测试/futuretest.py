#! /usr/bin/env python
#coding=utf-8

import tornado.web
import tornado.ioloop

from tornado.gen import coroutine
from tornado.concurrent import Future


def test():
    def pp(s):
        print s

    func_1 = lambda f: pp('ioloop callback after future done,future is %s'%f)

    def func_2(f):
        pp('ioloop callback after future done,future is %s'%f)
        print (a)

    future = Future()
    iol = tornado.ioloop.IOLoop.instance()

    print 'init future %s'%future

    iol.add_future(future, func_2)
    # iol.add_future(future, lambda f: pp('ioloop callback after future done,future is %s'%f))


    #模拟io延迟操作
    iol.add_timeout(iol.time()+5,lambda:future.set_result('set future is done'))

    print 'init complete'
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    test()