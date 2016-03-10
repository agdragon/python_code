# python urllib2使用ProxyHandler通过代理访问网页

标签（空格分隔）： python

---

在urllib2包中有ProxyHandler类，通过此类可以设置代理访问网页，如下代码片段：
```
#coding=utf8

import urllib2

proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8087'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://feeds2.feedburner.com/MobileOrchard')

print response.read()
```
使用本机8087端口的代理访问feedburner的内容。




