#!/usr/bin/python
#coding=utf-8
import redis

if __name__ == "__main__":
	data  = dict(name3=3.3, name4=4.4, name5=5.5)
	print type(data)
	r = redis.StrictRedis(host="localhost", port=6379, db=0)
	r.zadd('my-key', 1.1, 'name1', 2.2, 'name2', name3=3.3, name4=4.4, name5=5.5)
	#r.zadd('my-key2', data)