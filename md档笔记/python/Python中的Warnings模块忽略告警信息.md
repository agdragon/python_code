# Python中的Warnings模块忽略告警信息

标签（空格分隔）： python

---

运行代码遇到警告信息，如何消除警告信息？
如果是直接运行脚本，在运行脚本时，可以加参数`-W ignore`,比如要运行代码`test.py`,就输入如下命令:
`python -W ignore test.py`
如果是打包成程序，则直接在代码开始处，加入下代码即可:
```
import warnings  
warnings.filterwarnings("ignore") 
```




