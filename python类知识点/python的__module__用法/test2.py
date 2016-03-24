import os,sys

from test1 import A

# a = A()
# print type(A.__module__)
print A.__module__



print A.__bases__

a = A(1)
print a.__class__