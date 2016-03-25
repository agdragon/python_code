#-*-ecoding=utf-8-*-
#!/usr/bin/env python

'''
#	Python通过re模块提供对正则表达式的支持。
#	使用re的一般步骤是:
#		1: 将正则表达式的字符串形式编译为Pattern实例
#		2: 使用Pattern实例处理文本并获得匹配结果（一个Match实例）
#		3: 使用Match实例获得信息，进行其他的操作
'''

import re
 
# 将正则表达式编译成Pattern对象
pattern = re.compile(r'hello')
 
# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
match = pattern.match('hello world!')
 
# 使用Match获得分组信息
print match.group()
 
### 输出 ###
# hello