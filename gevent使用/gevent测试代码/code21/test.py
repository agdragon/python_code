from gevent import core
import gevent.hub
import time

loop = gevent.hub.get_hub().loop

print loop

def hello_world():
    print "%s : hi" % (time.time())

def lazy_hello_world():
    print "%s : lazy" % (time.time())

loop.run_callback(hello_world)

timer = loop.timer(3)

timer.start(lazy_hello_world)

print loop

loop.run()