import gevent
from multiprocessing import Process, Pipe
from gevent.socket import wait_read, wait_write

a_send,a_recv= Pipe()

def relay():
    for i in range(10):
        msg = a_recv.recv()
        print msg
        

def put_msg():
    for i in range(10):
        wait_write(a_send.fileno())
        a_send.send('hi')


proc = Process(target=relay)
proc.start()

g1 = gevent.spawn(put_msg)
gevent.joinall([g1], timeout=1)

