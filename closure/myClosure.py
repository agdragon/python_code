#!/usr/bin/python
#coding=utf-8

#内层函数引用了外层函数的变量,然后返回内层函数的情况就是闭包

def functionA():
	fs = []
	for i in range(1, 4):
		def f(j):
			def g():
				return j*j
			return g
		fs.append(f(i))
	return fs

def functionB():
	fs = []
	for i in range(1, 4):
		def f():
			return i*i
		fs.append(f)
	return fs

def line_conf():
    b = 15
    def line(x):
        return 2*x+b
    return line       # return a function object

if __name__ == "__main__":
	'''
	f1, f2, f3 = functionB()
	print f1()
	print f2()
	print f3()
	'''
	
	b = 5
	my_line = line_conf()
	print(my_line.__closure__)
	print(my_line.__closure__[0].cell_contents)