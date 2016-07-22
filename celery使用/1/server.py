#!/usr/bin/env python
# encoding: utf-8

from tornado import gen
from tornado import ioloop
from tornado.web import asynchronous, RequestHandler, Application

import tasks
import tcelery
tcelery.setup_nonblocking_producer()



class AsyncHandler(RequestHandler):
    def initialize(self, name):
        self.name = name

    @asynchronous
    def get(self):
        # tasks.add.apply_async(args=[3,8], callback=self.on_result)
        x = self.get_argument("x", 100)
        y = self.get_argument("y", 200)

        result = tasks.taskA.delay(int(x), int(y))
        self.write(result.state)
        self.finish()


    def on_result(self, response):
        self.write(str(response.result))
        self.finish()

class sleepHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        tmp = self.get_argument("tmp",200)
        response = yield gen.Task(tasks.sleep.apply_async, args=[tmp])
        self.write(str(response.result))
        self.finish()

application = Application([
    (r"/add", AsyncHandler, dict(name="xds")),
    (r"/sleepTask", sleepHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    ioloop.IOLoop.instance().start()

