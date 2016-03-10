# python - __dict__的妙用

标签（空格分隔）： python

---

设想这样一个场景。
我有一个字典，从某个地方获取的，比如http请求发过来的，比如从redis中hgetall出来的。我要根据这个字典来构建一个对象。
比如类:
```
class Person:
    def __init__(self,_obj):
        self.name = _obj['name']
        self.age = _obj['age']
        self.energy = _obj['energy']
        self.gender = _obj['gender']
        self.email = _obj['email']
        self.phone = _obj['phone']
        self.country = _obj['country']
```

利用`__dict__`的特性，上面的类可以用如下的代替，代码量大大减少:
```
class Person:
    def __init__(self,_obj):
        self.__dict__.update(_obj)
```





