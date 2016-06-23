#!/usr/bin/env python
#coding=utf-8

class UnknownDB(Exception):
    """raised for unsupported dbms"""
    pass

def database():
    name = "xds"
    if name != "xds":
        print name
    else:
        raise UnknownDB, name

if __name__ == '__main__':
	try:
		database()
	except UnknownDB, e:
		print e