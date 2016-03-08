#! /usr/bin/env python
#coding=utf-8

import tornado.web
import tornado.ioloop

from tornado.gen import coroutine
from tornado.concurrent import Future


from tornado.stack_context import (StackContext, wrap, NullContext, StackContextInconsistentError,
                                   ExceptionStackContext, run_with_stack_context, _state)


def test():
    def pp(s):
        print s

    future = Future()
    iol = tornado.ioloop.IOLoop.instance()

    print 'init future %s'%future

    def callback(f):
        pp('ioloop callback after future done,future is %s'%f)

    def callback_1(a,b):
        pp('ioloop callback_1 after future done,future is %s'%a)

    iol.add_future(future, callback)
    # iol.add_future(future, lambda f: pp('ioloop callback after future done,future is %s'%f))

    #模拟io延迟操作
    iol.add_timeout(iol.time()+5,lambda:future.set_result('set future is done'))

    print 'init complete'
    tornado.ioloop.IOLoop.instance().start()

def pp(s):
        print s

def callback(f):
    pp('ioloop callback after future done,future is %s'%f)

if __name__ == "__main__":
    # print wrap(callback)
    # print wrap(callback)
    test()
