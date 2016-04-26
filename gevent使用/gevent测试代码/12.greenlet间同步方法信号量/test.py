import gevent
from gevent.pool import Pool
from gevent.lock import BoundedSemaphore

sem = BoundedSemaphore(2)

def worker1(n):
    sem.acquire()
    print('worker %d acquire sem' %n)
    gevent.sleep(0)
    sem.release()
    print('woker %d release sem' %n)

def worker2(n):
    with sem:
        print('worker2 %d acquire sem' %n)
        gevent.sleep(0)
    print('woker2 %d release sem' %n)

pool = Pool()
pool.map(worker1, xrange(0,5))
# pool.map(worker2, xrange(0,5))