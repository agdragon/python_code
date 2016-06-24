#!/usr/bin/env python
#coding=utf-8

class UnknownName(Exception):
    """raised for unsupported dbms"""
    code = 1001
    pass

class Http404(Exception):
    def __init__(self, msg):
        super(Http404, self).__init__(msg)
        self.msg = msg
        print msg


def database():
    name = "xds"
    if name != "xds":
        print name
    else:
        raise UnknownName

def database_1():
    name = "xds"
    if name != "xds":
        print name
    else:
        raise Http404(name)



if __name__ == '__main__':
	try:
		database_1()
	except Http404:
		print Http404
