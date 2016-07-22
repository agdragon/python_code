#!/usr/bin/env python
#coding=utf-8

class Http404(Exception):
    def __init__(self, msg):
        super(Http404, self).__init__(msg)
        print type(msg)
        print msg["a"]
        self.msg = msg

def database_1():
    msg = {
        "a":1
    }
    if len(msg) < 0:
        print msg
        pass
    else:
        raise Http404(msg)



if __name__ == '__main__':
    try:
        database_1()
    except Http404, msg:
        print (msg.msg["a"])
