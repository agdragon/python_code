# python的callable(object)函数

标签（空格分隔）： python

---

# callable(object)函数:
中文说明：检查对象object是否可调用。如果返回True，object仍然可能调用失败；但如果返回False，调用对象ojbect绝对不会成功。
注意：类是可调用的，而类的实例实现了`__call__()`方法才可调用。
版本：该函数在python2.x版本中都可用。但是在python3.0版本中被移除，而在python3.2以后版本中被重新添加。
```
>>> callable(0)
False
>>> callable("mystring")
False
>>> def add(a, b):
…     return a + b
…
>>> callable(add)
True
>>> class A:
…      def method(self):
…         return 0
…
>>> callable(A)
True
>>> a = A()
>>> callable(a)
False
>>> class B:
…     def __call__(self):
…         return 0
…
>>> callable(B)
True
>>> b = B()
>>> callable(b)
True
```




