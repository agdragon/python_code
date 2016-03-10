# python中os.path.dirname(__file__)的使用

标签（空格分隔）： python

---

(1).当`print os.path.dirname(__file__)`所在脚本是以完整路径被运行的， 那么将输出该脚本所在的完整路径，比如：
```
python d:/pythonSrc/test/test.py
```
那么将输出: `d:/pythonSrc/test`

(2).当`print os.path.dirname(__file__)`所在脚本是以相对路径被运行的， 那么将输出空目录，比如：
```
python test.py
```
那么将输出空字符串




