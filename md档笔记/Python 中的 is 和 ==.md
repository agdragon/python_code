﻿# Python 中的 is 和 ==

标签（空格分隔）： python

---

以前在学Java时，记得判断字符串是否相等要用equals(str)方法，而不能直接用==。equals判断的是值是否相同，==判断的是引用是否相同。内容相同的两个字符串其引用可能是不同的。

今天在用Python时，也刚好遇到判断字符串是否相等的问题，纠结了一下，想知道Python中字符串是否有equals方法，但是并没有找到。在StackOverFLow上看到一篇讨论也是这个问题，有两个回答写得挺好的。

The operator a is b returns True if a and b are bound to the same object, otherwise False. When you create two empty lists you get two different objects, so is returns False (and therefore is notreturns True).

is is the identity comparison. #比较引用是否相同

== is the equality comparison. #比较内容是否相同
```
[] is []
False
[] == []
True
```

python中新建变量时，并不需要指定类型，因为每个变量实际上存储的是一个引用，就是指向一个对象实体的指针。

is 判断的就是这个指针的值是否相同，如果相同则表示两个变量指向同一个对象实体。

而==则比较它们的内容是否相同，这一点与Java中的String不同。



