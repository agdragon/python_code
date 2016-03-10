# python中关于with及contextlib的用法

标签（空格分隔）： python

---

平常Coding过程中，经常使用到的with场景是（打开文件进行文件处理，然后隐式地执行了文件句柄的关闭，同样适合socket之类的，这些类都提供了对with的支持）:
```
with file('test.py','r') as f :
    print f.readline()
```

`with`的作用，类似`try...finally...`，提供一种上下文机制，要应用`with`语句的类，其内部必须提供两个内置函数`__enter__`以及`__exit__`。前者在主体代码执行前执行，后则在主体代码执行后执行。`as`后面的变量，是在`__enter__`函数中返回的。通过下面这个代码片段以及注释说明，可以清晰明白`__enter__`与`__exit__`的用法：
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys

class echo :
	def output(self) :
		print 'hello world'
	def __enter__(self):
		print 'enter'
		return self #返回自身实例，当然也可以返回任何希望返回的东西
	def __exit__(self, exception_type, exception_value, exception_traceback):
		#若发生异常，会在这里捕捉到，可以进行异常处理
		print 'exit'
		#如果改__exit__可以处理改异常则通过返回True告知该异常不必传播，否则返回False
		if exception_type == ValueError :
			return True
		else:
			return False


def main():
	with echo() as e:
		e.output()
		print 'do something inside'

	print '-----------'
	
	with echo() as e:
		raise ValueError('value error')
	print '-----------'
	with echo() as e:
		raise Exception('can not detect')



if __name__ == '__main__':
	main()
```
执行结果:
```
enter
hello world
do something inside
exit
-----------
enter
exit
-----------
enter
exit
Traceback (most recent call last):
  File "warningTest.py", line 38, in <module>
    main()
  File "warningTest.py", line 33, in main
    raise Exception('can not detect')
Exception: can not detect
```



