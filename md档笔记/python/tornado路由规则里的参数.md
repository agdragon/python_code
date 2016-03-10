# tornado路由规则里的参数

标签（空格分隔）： tornado

---

路由表是 `URLSpec` 对象(或元组)的列表.

```
#!/usr/bin/env python 
# -*- coding:utf-8 -*- 


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import url
import tornado.httpclient

import time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class StoryHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db
        print "#"*10
        print self.db

    def get(self, story_id):
        self.write("this is story %s" % story_id)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            url(r"/story/([0-9]+)", StoryHandler, dict(db="db"), name="story")
            ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
```
分析:
`url(r"/story/([0-9]+)", StoryHandler, dict(db="db"), name="story")`:
1. `([0-9]+)`匹配到`def get(self, story_id)`中的`story_id`
2. `dict(db="db")`匹配到`initialize(self, db)`中的`db`
3. `name="story` Used by `Application.reverse_url`.


