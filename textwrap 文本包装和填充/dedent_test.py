#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# @author   xubigshu@gmail.com
# @date     2016-3-25
# @desc     fill(text, width=70, **kwargs) :文本进行不缩进显示，相应的indent()方法 -> 进行缩进显示
#


from textwrap import *

#dedent()方法
def test_wrap():
    test_str = '''\
    The textwrap module provides two convenience
        functions, wrap() and fill(), as well as 1
    TextWrapper, the class that does all the work,
        and two utility functions, dedent() and indent(). If 2
    you’re just wrapping or filling one or two text strings,
        the convenience functions should be good 3
    enough; otherwise, you should use an instance
        of TextWrapper for efficiency. 4
    '''
    print(repr(dedent(test_str)))

def main():
    test_wrap()

if __name__ == '__main__':
    main()