import tornado.ioloop
import tornado.web
from tornado.gen import coroutine

from tasks import test
import torncelery

from tornado.options import define, options
define("debug", default=True, type=bool)

class MainHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        result = yield torncelery.async(test, "hello world", callback=self.test)
        # self.write("%s" % result )

    def test(self, result):
        print "result: %s" % result
        self.write("%s" % result )


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()