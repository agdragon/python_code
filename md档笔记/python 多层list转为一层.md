# python 多层list转为一层

标签（空格分隔）： python

---

在c，c++等语言中可以通过多层嵌套的list来讲多维list转换为二维list
```
for inner_list in outer_list:
    for item in inner_list:
        ...
```

而在python中我们可以使用list强大的推导式来完成相同的工作：
```
ll = [[1,2,3],[2,3,4,5]]
l = [i for inner in ll for i in inner]
print l
[1, 2, 3, 2, 3, 4, 5]
```

如果你觉得推导不好理解，也可以用itertools来实现，如下代码：
```
list_of_menuitems = [['image00', 'image01'], ['image10'], []]
import itertools
chain = itertools.chain(*list_of_menuitems)
```




