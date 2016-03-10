# python的yield

标签（空格分隔）： python

---

```
#!/usr/bin/env python
#coding=utf-8

import time

def consumer():
	r = ""
	while True:
		n = yield r
		if not n:
			return
		print "consumer: %s"%(n)
		time.sleep(1)
		r = "200  ok"

def produce(c):
    c.next()	#启动生成器

    n = 0
    while n<5:
    	n += 1
    	print "produce: %s"%(n)
    	r = c.send(n)
    	print "consumer return %s"%(r)

    c.close()


if __name__=='__main__':
    c = consumer()
    produce(c)
```




