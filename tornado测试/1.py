#!/usr/bin/env python 
# -*- coding:utf-8 -*- 

'''
# add_handlers
'''

import tornado.ioloop
import tornado.web
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
 
class DomainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, a.com")
 
 
application = tornado.web.Application([
    (r"/", MainHandler),
])
 
application.add_handlers(r"^a\.com$", [(r"/", DomainHandler),])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()