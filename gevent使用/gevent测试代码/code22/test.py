import gevent
from gevent import Greenlet


class G1(Greenlet):
    def __init__(self):
        Greenlet.__init__(self)

    def switch_out(self):
        print 'switch_out'

    def _run(self):
        print 'run1'
        #gevent.sleep(0)
        print 'run2'

g = G1()
g.start()
g.join()
        