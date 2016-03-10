# python `__slots__`作用

标签（空格分隔）： python

---

`python`新模式的`class`，即从`object`继承下来的类有一个变量是`__slots__`，`slots`的作用是阻止在实例化类时为实例分配`dict`，默认情况下每个类都会有一个`dict`,通`过__dict__`访问，这个`dict`维护了这个实例的所有属性，举例如下
```
class base(object):
    v = 1
    def __init__(self):
          pass
          
b = base()
print b.__dict__
b.x = 2                     #可以增加新的变量
print b.__dict__
运行：
{}
{'x':2}
```
可见：实例的`dict`只保持实例的变量，对于类的属性是不保存的，类的属性包括变量和函数。由于每次实例化一个类都要分配一个新的`dict`，因此存在空间的浪费，因此有了`slots`，当定义了`slots`后，`slots`中定义的变量变成了类的描述符，相当于java，c++中的成员变量声明，类的实例只能拥有这些个变量，而不在有`dict`，因此也就不能在增加新的变量
```
class base(object):
   __slots__ = ('y')
    v = 1
    def __init__(self):
          pass

b = base()
print b.__dict__
b.x = 2              #error,不能增加新的变量 (任何试图创建一个其名不在__slots__中的名字的实例属性都将导致AttributeError异常)
print b.__dict__
```
注意，如果类的成员变量与slots中的变量同名:
```
class base(object):
    __slots=('y',)
    y = 2
    v = 1
    def __init__(self):
          pass

b = base()
print b.__dict__
b.x = 2
b.y = 3 //read only
print b.__dict__
```
目前的实现是该变量被设置为readonly！！！



## 对python的`__slots__`的研究 ##

---
今天在网上看到这样一个帖子，说的是python中__slots__的问题。
代码1:
```
class A(object):
    pass

class B(A):
    __slots__='b'

x=B()
x.e=2
```
这里并没有抛出异常，照理说`e`并不在`__slots__`的列表里，`__slots__`列表里也没有`__dict__`，应该会抛出异常才对。
看到这个帖子中的问题我也感到很疑惑，的确，这似乎和`python`文档中的描述不一致,于是我有写了下面这样一段代码:
代码2:
```
class C(int):
    __slots__='c'

y=C()
y.c=1
y.e=2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'C' object has no attribute 'e'
```
很奇怪，这里又抛出了异常。问题出在哪里？难道是`int`和`class A`有什么不同。
进入`python`源码分析。

先看看执行`代码1`中`x.e`时，`python`都做了什么:
当执行`x.e`时`python`会调用`PyObject_GenericGetAttr(PyObject *obj, PyObject *name)(object.c文件`)来查找`x.e`的值,这个函数有好几个返回点，通过在每个返回点（即`goto done;`语句前）添加`printf`输出可以看到`x.e`会在这段代码执行后返回：
```        
dictoffset = tp->tp_dictoffset;
if (dictoffset != 0) {
    //添加的额外输出
    printf("got value here_4!\n");
    goto done;
}
Py_DECREF(dict);
```
而实验后发现`代码2`中`y.e`无法进入上面的`if`语句。由此可见`tp_dictoffset`等不等于`0`是这个问题的关键，`x.e`没抛出异常正是由于它的这个值不为零，而`y.e`这事因为这个值为零了而强行给`y.e`赋值造成的。实际上通过阅读代码可以发现`tp_dictoffset`正是为了用来帮助`python`虚拟机找的实例对象的`tp_dict`的指针用的，在`ty_dict`中保存了实例独有的属性。于是现在问题转为`了tp_dictoffset`到底什么时候为`0`,什么时候不为`0`。
而这个值在`class B`和`class C`定义好后就确定下来了。
将目光转向`class B`和`class C`创建的时候。`class B`和`class C`由`type_new`函数`(typeobject.c中)`创建。通过对源码的阅读发现，影响到`tp_dictoffset`值的关键变量有如下两个：
```
may_add_dict//初始值为base->tp_dictoffset == 0，base为创建类（type）的主父类
add_dict//该值确定了到底要不要设定tp_dictoffset的值
```
在`type`的父类列表里的类（除去主父类）的`tp_dictoffset`值不为零时都将设定`type`的`tp_dictoffset`值（此外还有一些情况也会设定），使其不为零。
但代码1是一个特例，在`class B`的构建过程中，在`type_new`函数中为`tp_dictoffset`赋值的代码段执行完后，它的`tp_dictoffset`任然为`0`：
```
if (add_dict) {
    if (base->tp_itemsize)
        type->tp_dictoffset = -(long)sizeof(PyObject *);
    else
        type->tp_dictoffset = slotoffset;
        slotoffset += sizeof(PyObject *);
    }
```
因为执行这段语句的时候`add_dict`为`0`,所以根本不会设定`tp_dictoffset`的值。事实上，`class B`这种情况并不是在`type_new`本身中设定了`tp_dictoffset`的值，而是在`type_new`最好，它调用函数`PyType_Ready`函数进行初始化，再由`PyType_Ready`调用函数`inherit_special`，在`inherit_special`的最后由语句`COPYVAL(tp_dictoffset)`;完成了对`tp_dictoffset`的设定。
# 总结：
事实上可以这样考虑这个问题：使用`__slots__`时，如果父类当中存`在__dict__`,则其将继承`__dict__`，于是执行`代码1`中的`x.e=2`这样的语句就不会抛出异常。而对于`int`这样的内建类型，我们认为它没有`__dict__`，因为查看源码可以看到`PyInt_Type`结构中，`tp_dictoffset`被设置成了`0`。
此外，在`type_new`函数的代码中我们也可以看到，在多继承情况下，非主父类中存在`__dict__`也将会被子类继承。
当然，不存在`__dict__`的类型不仅仅只有内建类型，用户定义的类型也可以不包含`__dict__`，比如将`代码1`中的类型`A`改为：
```
class A(object):
    __slots__=('a','b')
```
这样以后执行到`x.e=2`也会抛出异常了。