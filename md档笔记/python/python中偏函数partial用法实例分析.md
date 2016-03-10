# python中偏函数partial用法实例分析

标签（空格分隔）： python

---

函数在执行时，要带上所有必要的参数进行调用。但是，有时参数可以在函数被调用之前提前获知。这种情况下，一个函数有一个或多个参数预先就能用上，以便函数能用更少的参数进行调用。
例如：
```
from functools import partial

def add(a,b):
    return a+b

add(4,3)
结果: 7

plus = partial(add,100)
plus(9)
结果: 109

plus2 = partial(add,99)
plus2(9)
结果: 108
```
其实就是函数调用的时候，有多个参数 参数，但是其中的一个参数已经知道了，我们可以通过这个参数重新绑定一个新的函数，然后去调用这个新函数。




