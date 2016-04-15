#gevent教程

###概述:
gevent是一个基于协程的python网络库。


##**内容**

* 目录：
    * [greenlet概述](#user-content-greenlet概述)
    * [父greenlet](#user-content-父greenlet)
    * [greenlet实例化](#user-content-greenlet实例化)
    * [在greenlets间切换](#user-content-在greenlets间切换)
    * [垂死的greenlet](#user-content-垂死的greenlet)
    * [gevent概述](#user-content-gevent概述)
    * [gevent的调度流程](#user-content-gevent的调度流程)
    


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

    `greenlet.getcurrent()`:

        返回当前`greenlet`,也就是谁在调用这个函数。

    `greenlet.GreenletExit`:

        这个特定的异常不会波及到父`greenlet`,它用于干掉一个`greenlet`。


* ####在greenlets间切换：
    `greenlet`之间的切换发生在`greenlet`的`switch()` 方法被调用时,这会让执行点跳转到`greenlet`的`switch()`被调用处.或者在`greenlet`死掉时,跳转到父`greenlet`那里去.在切换时,一个对象或异常被发送到目标`greenlet`.这可以作为两个`greenlet`之间传递信息的方便方式.

    例如:

        #!/usr/bin/python
        #coding=utf-8

        from greenlet import greenlet

        def test1(x,y):
            z=gr2.switch(x+y)
            print z

        def test2(u):
            print u
            gr1.switch(42)

        gr1=greenlet(test1)
        gr2=greenlet(test2)
        gr1.switch("hello"," world")

    结果:

        hello world
        42

    注意:

        test1() 和 test2() 的参数并不是在 greenlet 创建时指定的，而是在第一次切换到这里时传递的。

* ####垂死的greenlet：
    如果一个`greenlet`的`run()`结束了,他会返回值到父`greenlet`.如果`run()`是异常终止的，异常会波及到父`greenlet`(除非是`greenlet.GreenletExit`异常,这种情况下异常会被捕捉并返回到父`greenlet`).

    除了上面的情况外,目标`greenlet`会接收到发送来的对象作为`switch()`的返回值.虽然`switch()`并不会立即返回,但是它仍然会在未来某一点上返回,当其他`greenlet`切换回来时.当这发生时,执行点恢复到`switch()`之后,而`switch()` 返回刚才调用者发送来的对象.这意味着`x=g.switch(y)` 会发送对象`y`到`g`,然后等着一个不知道是谁发来的对象,并在这里返回给`x`。

    注意，任何尝试切换到死掉的`greenlet`的行为都会切换到死掉`greenlet`的父`greenlet`,或者父的父,等等。最终的父就是`main greenlet`,永远不会死掉的

* ####gevent概述：
    `gevent`是一个高性能网络库,底层是`libevent`,`1.0`版本之后是`libev`,核心是`greenlet`.`gevent`和`eventlet`是亲近,唯一不同的是`eventlet`是自己实现的事件驱动,而`gevent`是使用`libev`.两者都有广泛的应用,如`openstack`底层网络通信使用`eventlet`,`goagent`是使用`gevent`.
* ####gevent的调度流程：
    要想理解`gevent`,首先要理解`gevent`的调度流程.`gevent`中有一个`hub`的概念,也就是下图的`MainThread`,用于调度所有其它的`greenlet`实例(下图`Coroutine`).

    其实`hub`也是一个`greenlet`,只不过特殊一些.

    看下图我们会发现每次从`hub`切换到一个`greenlet`后,都会回到`hub`,这就是`gevent`的关键.

    注意:`gevent`中并没有`greenlet`链的说法,所有都是向主循环注册`greenlet.switch`方法,主循环在合适的时机切换回来.

    ![gevent执行流程](http://img2.ph.126.net/J6-XDpFxBjpsaThULXepzg==/2872733612409913241.jpg)