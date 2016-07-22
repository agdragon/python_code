#!/usr/bin/python
# -*- coding: utf-8 -*-
"""web main"""
import os
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, authenticated
from tornado.escape import json_encode

from jsonphandler import JSONPHandler


class MainHandler(RequestHandler):
    def get(self):
        # self.write("xds")
        self.render("index.html")
        
class TestJSONP(JSONPHandler):
    def get(self):
        self.write(json_encode({'josnp-get': 'hello world.'}))
        
    def post(self):
        self.write(json_encode({'josnp-post': 'hello world.'}))
        

settings = {
    "static_path":os.path.join(os.path.dirname(__file__), "static"),
    "template_path":os.path.join(os.path.dirname(__file__), 'templates'),
}

# settings = {
#     "template_path": "templates",
# }

application = Application([
    (r"/", MainHandler),
    (r"/jsonp/helloword", TestJSONP),
], **settings)


if __name__ == "__main__":
    print 'start'
    http_server = HTTPServer(application)
    http_server.listen(8081)
    IOLoop.instance().start()