# Python中`__class__`的理解

标签（空格分隔）： python

---

先运行下面一段代码：
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys

class A:
	def __init__(self,url):
		self.url = url
	def out(self):
		return self.url


def main():
	a = A('news.163.com')
	print a.out()

	b = a.__class__('www.bccn.net')
	print b.out()

	print "*****************"

	print A
	print a.__class__



if __name__ == '__main__':
	main()
```
输出:
```
news.163.com
www.bccn.net
*****************
__main__.A
__main__.A
```
结论:
可以看出`a.__class__`就等效于`a`的`类A`




