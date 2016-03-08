#!/usr/bin/python
# coding=utf-8

import time, datetime
import base64
from time import strftime

TIME_FORMAT = '%Y%m%dT%H%M%SZ'
TIME_FORMAT_1 = '%Y%m%d%H%M%S'

def get_current_local_time():
	local = datetime.datetime.now()
	return local.strftime(TIME_FORMAT_1)

def get_current_utc_time():
	utc = datetime.datetime.utcnow()
	return utc.strftime(TIME_FORMAT)
	newList = []
	for x in old_list:
		if x not in newList :
			newList.append(x)
	return newList

if __name__ == "__main__":
	a = str(get_current_local_time())
	b = base64.encodestring(a)
	c = base64.b64encode(a)
	d = base64.b16encode(a)
	
	print a
	print b
	print c
	print d


