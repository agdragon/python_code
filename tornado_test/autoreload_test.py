#!/usr/bin/env python 
# -*- coding:utf-8 -*- 

'''
tornado 自动加载（autoreload）
'''


'''
	#-----------------------------------------------#
	常规用法
	#-----------------------------------------------#
'''
import tornado.autoreload
def main():
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8888)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()



'''
	#-----------------------------------------------#
	改进用法
	#-----------------------------------------------#
'''
settings = {'debug' : True}
application = tornado.web.Application([
     (r"/", MainHandler),
     ], **settings)

def main():
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

'''
这是因为web.py中有如下定义:
'''
# Automatically reload modified modules
if self.settings.get("debug") and not wsgi:
    import autoreload
    autoreload.start()