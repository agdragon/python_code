import tornado.web
from greenlet_tornado import greenlet_asynchronous, greenlet_fetch
    
class ExampleHandler(tornado.web.RequestHandler):
    @greenlet_asynchronous
    def get(self):
        # ...
        self.helper()
        # ...
        self.write("Hello World!")

    def helper(self):
        # Fetch something. greenlet_fetch() will block until the request is complete,
        # but the tornado IOLoop can do other things in the meantime.
        http_response = greenlet_fetch("http://www.mopub.com")
        # ... Do something with the response ...