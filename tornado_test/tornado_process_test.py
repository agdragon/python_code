#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process


class LongHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(str(os.getpid()))
        time.sleep(10)


if __name__ == "__main__":
    app = tornado.web.Application(([r'/', LongHandler], ))
    sockets = tornado.netutil.bind_sockets(8090)
    tornado.process.fork_processes(2)
    server = tornado.httpserver.HTTPServer(app)
    server.add_sockets(sockets)
    tornado.ioloop.IOLoop.instance().start()

'''
https://www.linuxzen.com/tornado-duo-jin-cheng-shi-xian-fen-xi.html
http://ju.outofmemory.cn/entry/118436
'''