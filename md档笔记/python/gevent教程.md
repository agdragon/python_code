#gevent教程

###概述:
gevent是一个基于协程的python网络库。


##**内容**

* 目录：
    * [greenlet概述](#user-content-greenlet概述)
    * [父greenlet](#user-content-父greenlet)
    * [greenlet实例化](#user-content-greenlet实例化)

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

        1: 最后一行首先跳转到 greenlet 之 gr1 执行其指定的函数 test1 ,这里 test1 没有参数，因此 gr1.switch() 也不需要指定参数。

        2: test1 打印 12 ,然后跳转到 test2 ,打印 56 ,然后跳转回 test1 ,打印 34 ,最后 test1 结束执行, gr1 死掉。这时执行会回到最初的 gr1.switch() 调用。

        3: 注意: 78 是不会被打印的。



* ####父greenlet：
    现在看看一个`greenlet`结束时执行点去哪里。每个`greenlet`拥有一个父`greenlet`。每个`greenlet`最初在其父`greenlet`中创建(不过可以在任何时候改变)。当子`greenlet`结束时,执行位置从父`greenlet`那里继续。这样,`greenlets`之间就被组织成一棵树,顶级的代码并不在用户创建的`greenlet`中运行,而是运行在一个主`greenlet`中,也就是所有`greenlet`关系图的树根。
    
    在上面的例子中,`gr1`和`gr2` 都把主`greenlet`作为父`greenlet`。任何一个死掉，执行点都会回到主`greenlet`。
    
    未捕获的异常会传递给父`greenlet`。如果上面的`test2`包含一个打印错误,会生成一个`NameError`而杀死`gr2`,然后异常被传递回主`greenlet`。`traceback`会显示`test2`而不是`test1`。记住,切换不是调用，而是执行点在并行的栈容器间交换，而父`greenlet`定义了这些栈之间的先后关系。


* ####greenlet实例化：
    `greenlet(run=None, parent=None)`:

    创建一个`greenlet`对象,不执行。`run`是这个`greenlet`要执行的回调函数,而`parent`是父`greenlet`,缺省为当前`greenlet`。


