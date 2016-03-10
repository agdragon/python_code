# tornado笔记

标签（空格分隔）： tornado

---

```
#!/usr/bin/env python
# coding=utf-8

import tornado.web
from base import BaseHandler

import time

class SleepHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 17, callback=self.on_response)
    def on_response(self):
        self.render("sleep.html")
        self.finish()
```
即在get()方法前面增加了装饰器@tornado.web.asynchronous，它的作用在于将tornado服务器本身默认的设置_auto_fininsh值修改为false。如果不用这个装饰器，客户端访问服务器的get()方法并得到返回值之后，两只之间的连接就断开了，但是用了@tornado.web.asynchronous之后，这个连接就不关闭，直到执行了self.finish()才关闭这个连接。




