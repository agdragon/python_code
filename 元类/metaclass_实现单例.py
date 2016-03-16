#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Singleton(type):
    def __init__(self,name,bases,class_dict):
        super(Singleton,self).__init__(name,bases,class_dict)
        self._instance=None
    def __call__(self,*args,**kwargs):
        if self._instance is None:
            self._instance=super(Singleton,self).__call__(*args,**kwargs)
        return self._instance

class A(object):
        __metaclass__ = Singleton 
        def __init__(self, x):
            self.x = x

if __name__=='__main__':
         
    a=A(1)
    b=A(2)
    print id(a),id(b)
    print a.x, b.x


'''
#-- 结果:
    
        25166160 25166160
        1 1

'''



'''
#-- 分析:
    
    __metaclass__顾名思义是class A的元类，所谓元类即其实例是一个类。所以，Singleton的一个实例是class A。那么A()到底是怎样的执行过程呢？ 
  
    1) Singleton实例化：隐式调用了Sinleton的__new__方法生成一个实例，并调用Singleton.__init__去初始化这个实例，初始化之后便产生了class A。这里，name, bases, dct就是class A的定义中的相关属性。
    2) A的实例化，由于在Singleton中定义了__call__，即Singleton的实例可以像函数一样调用。然而，Singleton的实例是class A，根据规则，在实例化A时即A()，解释器选择调用Singleton.__call__（并不调用A.__new__和A.__init__）。那么A.__init__在何时调用呢？
    3) 在执行Singleton.__Call__时，如果self.instance（即A.instance）是None时，则调用super(Singleton, self).__call__，在这个函数中会调用A.__init__,初始化A的实例后存在self.instance（即A.instance）中。

   通过这样就可以做到只有一个A的实例，并存储在A.instance中。元类确实有点绕人，但是弄清楚了之后，它在特定的时刻能带来很大的方便。 

'''