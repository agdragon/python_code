#!/usr/bin/python
#coding=utf-8

from contextlib import contextmanager
from contextlib import nested
from contextlib import closing

# '''
# #- 	contextlib是为了加强with语句，提供上下文机制的模块，它是通过Generator实现的。通过定义类以及写__enter__和__exit__来进行上下文管理虽然不难，但是很繁琐。
# #- 	contextlib中的contextmanager作为装饰器来提供一种针对函数级别的上下文管理机制。常用框架如下：
# '''

@contextmanager
def make_context() :
    print 'enter'
    
    yield {}
    
    print 'exit'

with make_context() as value :
    print value
'''
#-- 结果
		enter
		{}
		exit
'''

print "************************"


'''
#-  contextlib还有连个重要的东西，一个是nested，一个是closing，前者用于创建嵌套的上下文，后则用于帮你执行定义好的close函数。
#-  但是nested已经过时了，因为with已经可以通过多个上下文的直接嵌套了。下面是一个例子：
'''

@contextmanager
def make_context(name) :
    print 'enter', name
    yield name
    print 'exit', name
  
with nested(make_context('A'), make_context('B')) as (a, b) :
    print a
    print b
'''
#-- 得到如下结果

		enter A
		enter B
		A
		B
		exit B
		exit A
'''


 
with make_context('A') as a, make_context('B') as b :
    print a
    print b
'''
#-- 得到如下结果

		enter A
		enter B
		A
		B
		exit B
		exit A
'''
  
class Door(object) :
    def open(self) :
        print 'Door is opened'
    def close(self) :
        print 'Door is closed'
  
with closing(Door()) as door :
    door.open()
'''
#-- 得到如下结果

		Door is opened
		Door is closed
'''