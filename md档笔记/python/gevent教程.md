#gevent教程

###概述:
gevent是一个基于协程的python网络库。


##**内容**

* 目录：
    * [greenlet概述](#user-content-greenlet概述)
    * [装饰器property](#user-content-装饰器property)
    * [结论](#user-content-结论)

<br>


* ####greenlet概述
    一个 `greenlet` 是一个小型的独立伪线程。可以把它想像成一些栈帧，栈底是初始调用的函数，而栈顶是当前`greenlet`的暂停位置。你使用`greenlet`创建一堆这样的堆栈，然后在他们之间跳转执行。跳转必须显式声明的：一个greenlet必须选择要跳转到的另一个`greenlet`,这会让前一个挂起，而后一个在此前挂起处恢复执行。不同`greenlets`之间的跳转称为切换(`switching`) 。
    
    当你创建一个`greenlet`时，它得到一个开始时为空的栈；当你第一次切换到它时，它会执行指定的函数，这 个函数可能会调用其他函数、切换跳出`greenlet`等等。当最终栈底的函数执行结束出栈时，这个`greenlet`的栈又变成空的，这个`greenlet`也就死掉了。`greenlet`也会因为一个未捕捉的异常死掉。
    
    代码示例:

            #!/usr/bin/python
            #coding=utf-8

            from greenlet import greenlet

            def test1():
                print 12
                gr2.switch()
                print 34

            def test2():
                print 56
                gr1.switch()
                print 78

            if __name__ == '__main__':
                gr1 = greenlet(test1)
                gr2 = greenlet(test2)
                gr1.switch()

    结果:

            12
            56
            34


    代码以及结果分析:

        - 最后一行首先跳转到`greenlet`之`gr1`执行其指定的函数`test1`,这里 `test1`没有参数，因此`gr1.switch()`也不需要指定参数。

        - `test1`打印`12`,然后跳转到`test2`,打印`56`,然后跳转回`test1`,打印`34`,最后  `test1`结束执行,`gr1`死掉。这时执行会回到最初的`gr1.switch()`调用。
        
        - 注意:`78`是不会被打印的。


    



* ####装饰器property：
    还记得装饰器`(decorator)`可以给函数动态加上功能吗？对于类的方法，装饰器一样起作用。`Python`内置的`@property`装饰器就是负责把一个方法变成属性调用的：

        ```
            class Student(object):
                @property
                def score(self):
                    return self._score

                @score.setter
                def score(self, value):
                    if not isinstance(value, int):
                        raise ValueError('score must be an integer!')
                    if value < 0 or value > 100:
                        raise ValueError('score must between 0 ~ 100!')
                    self._score = value
        ```

    `@property`的实现比较复杂，我们先考察如何使用。把一个`getter`方法变成属性，只需要加上`@property`就可以了，此时，`@property`本身又创建了另一个装饰器`@score.setter`，负责把一个`setter`方法变成属性赋值，于是，我们就拥有一个可控的属性操作：

        ```
            s = Student()
            s.score = 60 # OK，实际转化为s.set_score(60)
            s.score # OK，实际转化为s.get_score()
            
            60
            
            s.score = 9999
            Traceback (most recent call last):
              ...
            ValueError: score must between 0 ~ 100!
        ```

    注意到这个神奇的`@property`，我们在对实例属性操作的时候，就知道该属性很可能不是直接暴露的，而是通过getter和setter方法来实现的。

    还可以定义只读属性，只定义`getter`方法，不定义`setter`方法就是一个只读属性：

        ```
            class Student(object):
                @property
                def birth(self):
                    return self._birth

                @birth.setter
                def birth(self, value):
                    self._birth = value

                @property
                def age(self):
                    return 2014 - self._birth
        ```
        
    上面的`birth`是可读写属性，而`age`就是一个只读属性，因为`age`可以根据`birth`和当前时间计算出来。


* ####结论：
    `@property`广泛应用在类的定义中，可以让调用者写出简短的代码，同时保证对参数进行必要的检查，这样，程序运行时就减少了出错的可能性。

