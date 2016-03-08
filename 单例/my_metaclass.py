#!/usr/bin/env python
#coding=utf-8

class Singleton2(type):  
    def __init__(self, name, bases, dct):  
        super(Singleton2, self).__init__(name, bases, dct)  
        self.instance = None  
  
    def __call__(self,*args,**kw):  
        if self.instance is None:  
            self.instance = super(Singleton2, self).__call__(*args, **kw)  
        return self.instance     
    
class MyClass(object):    
    __metaclass__ = Singleton2    
    
one = MyClass()    
two = MyClass()    
    
two.a = 3    
print one.a    
  
print id(one)    
print id(two)    
   
print one == two    
   
print one is two      