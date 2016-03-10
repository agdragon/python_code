# 理解Python中super()和__init__()方法

标签（空格分隔）： python

---

我试着理解super()方法.从表面上看,两个子类实现的功能都一样.我想问它们俩的区别在哪里?
```
class Base(object):
    def __init__(self):
        print "Base created"

class ChildA(Base):
    def __init__(self):
        Base.__init__(self)

class ChildB(Base):
    def __init__(self):
        super(ChildB, self).__init__()

print ChildA(),ChildB()
```
`super()`的好处就是可以避免直接使用父类的名字.但是它主要用于多重继承,这里面有很多好玩的东西.如果还不了解的话可以看看官方文档




