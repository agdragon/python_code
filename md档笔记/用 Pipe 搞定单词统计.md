# 用 Pipe 搞定单词统计

标签（空格分隔）： python

---
题目：
读取文件，统计文件中每个单词出现的次数，然后按照次数高低排序。

代码:
```
from __future__ import print_function
from re import split
from pipe import *
with open('test_descriptor.py') as f:
  print(f.read()
        | Pipe(lambda x:split('/W+', x))
        | Pipe(lambda x:(i for i in x if i.strip()))
        | groupby(lambda x:x)
        | select(lambda x:(x[0], (x[1] | count)))
        | sort(key=lambda x:x[1], reverse=True)
        )
```
输出：
```
[('self', 13), ('foo', 9), ('item', 9), ('_data', 8), ('print', 7), ('def', 5), ('return', 5), ('Jeff', 4), ('i', 4), ('in', 4), ('jeff', 4), ('ken', 4), ('obj', 4), ('val', 4), ('class', 3), ('lai', 3), ('pan', 3), ('tmp', 3), ('Foo', 2), ('ItemDescriptor', 2), ('Wrapper', 2), ('__iter__', 2), ('for', 2), ('if', 2), ('next', 2), ('object', 2), ('0', 1), ('1', 1), ('30', 1), ('8', 1), ('None', 1), ('__class__', 1), ('__future__', 1), ('__get__', 1), ('__init__', 1), ('__set__', 1), ('bin', 1), ('coding', 1), ('env', 1), ('f', 1), ('from', 1), ('import', 1), ('instance', 1), ('isinstance', 1), ('len', 1), ('list', 1), ('print_function', 1), ('python', 1), ('type', 1), ('usr', 1), ('utf', 1)]
```


