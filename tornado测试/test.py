#!/usr/bin/env python 
# -*- coding:utf-8 -*- 

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import url
from tornado.web import URLSpec
import tornado.httpclient

from tornado.ioloop import PeriodicCallback

import time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("story", "1"))

class StoryHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db
        print "#"*10
        print self.db

    def get(self, story_id):
        self.write("this is story %s" % story_id)


class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        time.sleep(5)
        self.write("when i sleep 5s")

class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you")

class DomainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, a.com")


def test_1():
    print "aaaaaaaaaaaa"

def test_2():
    print "bbbbbbbbbbbb"
    print tornado.ioloop.IOLoop.instance().time()


handlerList = [
            url(r"/sleep", SleepHandler),
            url(r"/justnow", JustNowHandler),
            url(r"/", MainHandler),
            url(r"/story/([0-9]+)", StoryHandler, dict(db="db"), name="story")
        ]

settingDict = {
            "static_path":os.path.join(os.path.dirname(__file__), "static"),
            "template_path":os.path.join(os.path.dirname(__file__), 'templates')
        }

class Application(tornado.web.Application):
    def __init__(self):
        handlers = handlerList
        settings = settingDict
        tornado.web.Application.__init__(self, handlers, **settings)
        
        # PeriodicCallback(test_1, 1000).start()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            url(r"/sleep", SleepHandler),
            url(r"/justnow", JustNowHandler),
            url(r"/", MainHandler),
            url(r"/story/([0-9]+)", StoryHandler, dict(db="db"), name="story")
            ])

    print "#"*20
    tmp = app.handlers[0][1][1]
    print type(tmp)
    print tmp
    
    print "#"*20

    app.add_handlers(r"^a\.com$", [(r"/", DomainHandler),])
    
    print "#"*20
    host_handlers = [(r"/", DomainHandler),]
    print host_handlers
    for spec in host_handlers:
        if isinstance(spec, (tuple, list)):
            assert len(spec) in (2, 3, 4)
            spec = URLSpec(*spec)
    print host_handlers
    print spec
    print "#"*20



    # PeriodicCallback(test_1, 1000).start()

    # tmp = tornado.ioloop.IOLoop.instance().time()
    # print tmp
    # tt = tornado.ioloop.IOLoop.instance().add_timeout(tmp + 5, test_2)
    
    # print "××××××××××××××××××××××××"
    # print tt
    # print type(tt)


    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

