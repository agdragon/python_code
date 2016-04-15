#!/usr/bin/python
#coding=utf-8

from greenlet import greenlet

def test1():
	print 12
	gr2.switch()
	print 34

def test2():
	print 56
	gr1.switch()
	print 78

if __name__ == '__main__':
	gr1 = greenlet(test1)
	gr2 = greenlet(test2)
	gr1.switch()
	
'''
最后一行首先跳转到greenlet  gr1 执行其指定的函数 test1,这里 test1没有参数，
因此 gr1.switch() 也不需要指定参数。 
test1打印12，然后跳转到  test2 ，打印56，然后跳转回 test1，打印34，
最后  test1 结束执行， gr1 死掉。这时执行会回到最初的  gr1.switch()  调用。
注意，78是不会被打印的。
'''