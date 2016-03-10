# python实现单例模式

标签（空格分隔）： python

---
通过`__metaclass__`来实现:
```
class Singleton(type):
    def __init__(self, name, bases, dct):
        super(Singleton, self).__init__(name, bases, dct)
        self.instance = None

    def __call__(self,*args,**kw):
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kw)
        return self.instance
class A(object):
    __metaclass__ = Singleton
    def __init__(self):
        self.xx = 1
A()
```
注解：
 `__metaclass__`顾名思义是`class A`的元类，`所谓元类即其实例是一个类`。所以，Singleton的一个实例是class A。那么A()到底是怎样的执行过程呢？ 
 

 1. `Singleton`实例化：
    隐式调用了`Sinleton`的`__new__`方法生成一个实例，并调用`Singleton.__init__`去初始化这个实例，初始化之后便产生了`class A`。这里`name, bases, dct`就是`class A`的定义中的相关属性。
 2. `A`的实例化
    由于在`Singleton`中定义了`__call__`，即`Singleton`的实例可以像函数一样调用。然而`Singleton`的实例是`class A`，根据规则，在实例化`A`时即`A()`，解释器选择调用`Singleton.__call__`（并不调用`A.__new__`和`A.__init__`）。那么`A.__init__`在何时调用呢？
 3. `A.__init__`调用
    在执行`Singleton.__Call__`时，如果`self.instance`（即`A.instance`）是`None`时，则调用`super(Singleton, self).__call__`，在这个函数中会调用`A.__init__`,初始化`A`的实例后存在`self.instance`（即`A.instance`）中。

---
通过`__new__`来实现:
```
class Singleton(object):
    def __new__(cls,*args,**kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst=super(Singleton,cls).__new__(cls,*args,**kwargs)
        return cls._inst
if __name__=='__main__':
    class A(Singleton):
        def __init__(self,s):
            self.s=s     
    a=A('apple')  
    b=A('banana')
    print id(a),a.s
    print id(b),b.s
```
结果：
```
29922256 banana
29922256 banana
```
通过`__new__`方法，将类的实例在创建的时候绑定到类属性`_inst`上。如果`cls._inst`为`None`，说明类还未实例化，实例化并将实例绑定到`cls._inst`，以后每次实例化的时候都返回第一次实例化创建的实例。注意从`Singleton`派生子类的时候，不要重载`__new__`。