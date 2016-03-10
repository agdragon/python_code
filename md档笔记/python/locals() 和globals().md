# locals() 和globals()

标签（空格分隔）： python

---

在函数外部，两者作用是一样。在函数内部时，locals()则是获取当前函数堆栈帧的名字空间，其中存储的是函数参数，局部变量等信息。

Python有两个内置的函数，locals() 和globals()，它们提供了基于字典的访问局部和全局变量的方式。

首先，是关于名字空间的一个名词解释。是枯燥，但是很重要，所以要耐心些。Python使用叫做名字空间的东西来记录变量的轨迹。名字空间只是一个 字典，它的键字就是变量名，字典的值就是那些变量的值。实际上，名字空间可以象Python的字典一样进行访问，一会我们就会看到。

在一个Python程序中的任何一个地方，都存在几个可用的名字空间。每个函数都有着自已的名字空间，叫做局部名字空间，它记录了函数的变量，包括 函数的参数和局部定义的变量。每个模块拥有它自已的名字空间，叫做全局名字空间，它记录了模块的变量，包括函数、类、其它导入的模块、模块级的变量和常 量。还有就是内置名字空间，任何模块均可访问它，它存放着内置的函数和异常。

当一行代码要使用变量 x 的值时，Python会到所有可用的名字空间去查找变量，按照如下顺序：

局部名字空间 - 特指当前函数或类的方法。如果函数定义了一个局部变量 x，Python将使用这个变量，然后停止搜索。
全局名字空间 - 特指当前的模块。如果模块定义了一个名为 x 的变量，函数或类，Python将使用这个变量然后停止搜索。
内置名字空间 - 对每个模块都是全局的。作为最后的尝试，Python将假设 x 是内置函数或变量。
如果Python在这些名字空间找不到 x，它将放弃查找并引发一个 NameError 的异常，同时传 递 There is no variable named 'x' 这样一条信息

象Python中的许多事情一样，名字空间在运行时直接可以访问。特别地，局部名字空间可以通过内置的 locals 函数来访问。全局（模块级别）名字空间可以通过 globals 函数来访问

- locals 介绍
```
>>> def test(arg):
#函数 foo 在它的局部名字空间中有两个变量：arg（它的值被传入函数），和 z（它是在函数里定义的）。
    z = 1
    print locals()
>>> test(4)
#locals 返回一个名字/值对的字典。这个字典的键字是字符串形式的变量名字，字典的值是变量的实际值。
#所以用 4 来调用 foo，会打印出包含函数两个局部变量的字典：arg (4) 和 z (1)。
{'z': 1, 'arg': 4}
>>> test('doulaixuexi')
#locals 可以用于所有类型的变量。
{'z': 1, 'arg': 'doulaixuexi'}
>>>
```

- globals 介绍
```
>>> from sys import *
>>> print globals()
{'setrecursionlimit': <built-in function setrecursionlimit>, 
'dont_write_bytecode': False, 
'getfilesystemencoding': <built-in function getfilesystemencoding>, 
'long_info': sys.long_info(bits_per_digit=15, sizeof_digit=2), 
'stdout': <idlelib.rpc.RPCProxy object at 0x02110850>, 
'text': <function text at 0x02111A70>, 
'meta_path': [], 
'exc_clear': <built-in function exc_clear>, 
'prefix': 'C:\\Python27', 'getrefcount': <built-in function getrefcount
```




