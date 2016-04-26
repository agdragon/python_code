import time
import threading

def hello(s):
    print s
    print time.time()

key = "xiaorui.cc"

print time.time()


t = threading.Timer(3.0, hello,[key])
t.start()

print t.isAlive()

print "aaaaaaaaaaaaa"


	