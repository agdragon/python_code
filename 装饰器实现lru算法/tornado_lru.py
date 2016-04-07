#!/usr/bin/env python 
# -*- coding:utf-8 -*- 

'''
# add_handlers
'''

import tornado.ioloop
import tornado.web
import time

"""
    #装饰器的妙用
"""


#定义一个登陆权限认证的装饰器
def log_test(f):
    root = []
    def _wrapper(self,*args, **kwargs):
        root.append("aaa")
        print root
        f(self, *args, **kwargs)
    return _wrapper


class MainHandler(tornado.web.RequestHandler):
    @log_test
    def get(self):
    	print "aaaaaaaaaaaa"
        self.write("Hello, world nihao")
 
class DomainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, a.com")

# 此时自动重新载入代码
settings = {'debug' : True}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/a", DomainHandler),
], **settings)
 
application.add_handlers(r"^a\.com$", [(r"/", DomainHandler),])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()