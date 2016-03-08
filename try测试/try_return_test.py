#!/usr/bin/env python 
# -*- coding:utf-8 -*- 

import os 

def b_func():
	print "b_func"
	return 1

def  a_func():
	try:
		a = 1
		b = 2
		return b_func()
	finally:
		return b

if __name__ == "__main__":
	print a_func()