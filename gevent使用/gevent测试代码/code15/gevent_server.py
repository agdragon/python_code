from gevent.server import StreamServer
import gevent
from gevent import monkey
monkey.patch_all()
import socket

from gevent import getcurrent

def handler(sock, addr):
    while True:
        data = sock.recv(1024)
        if not data:
            print addr, " closed"
            return
        print getcurrent(), "get: ",data


server = StreamServer(('localhost', 5000), handler)
server.serve_forever()