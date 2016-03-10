# 使用traceback获取详细的异常信息

标签（空格分隔）： python

---

```
try:
    1/0
except Exception,e:
    print e
```
输出结果是:
```
integer division or modulo by zero
```
只知道是报了这个错，但是却不知道在哪个文件哪个函数哪一行报的错

下面使用`traceback`模块
```
import traceback
try:
    1/0
except Exception,e:
    traceback.print_exc()
```
输出结果是:
```
Traceback (most recent call last):
File "test_traceback.py", line 3, in <module> 1/0
ZeroDivisionError: integer division or modulo by zero
```
这样非常直观有利于调试。

`raceback.print_exc()`跟`traceback.format_exc()`有什么区别呢？
`format_exc()`返回字符串，`print_exc()`则直接给打印出来。
即`traceback.print_exc()`与`print traceback.format_exc()`效果是一样的。
`print_exc()`还可以接受`file`参数直接写入到一个文件。比如
`traceback.print_exc(file=open('tb.txt','w+'))`
写入到`tb.txt`文件去。
