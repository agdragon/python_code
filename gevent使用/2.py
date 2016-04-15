import gevent

def talk(msg):
    print(msg)
    gevent.sleep(0)
    print msg

g1 = gevent.spawn(talk, 'bar')
gevent.sleep(0)