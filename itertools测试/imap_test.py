#! /usr/bin/env python
#coding=utf-8

from itertools import *

print 'Doubles:'
a = imap(lambda x:2*x, xrange(5))
b = imap(None, xrange(5))

print a
print type(a)
a = list(a)
print a

for i in a:
    print i

for i in b:
    print i

# print 'Multiples:'
# for i in imap(lambda x,y:(x, y, x*y), xrange(5), xrange(5,10)):
#     print '%d * %d = %d' % i