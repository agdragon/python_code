#stack_context分析

###概述:
`StackContext` allows applications to maintain threadlocal-like state that follows execution as it moves to other execution contexts
(这句话摘在tornado源码)


##**内容**

* 目录：
    * [抛出问题](#user-content-抛出问题)
    * [解决问题](#user-content-解决问题)
    * [tornado的解决方法](#user-content-tornado的解决方法)

<br>


* ####抛出问题：
    有如下代码:

        def dosomething():
            def do_cb():
                raise ValueException()

            try:
                do_async(callback=do_cb)
            except ValueException:
                deal_with_exception()

    上面的方法里`try…except`能捕获到`do_async`抛出的`ValueException`异常,但是不能捕获`do_cb`中抛出的异常。
    因为`do_cb`并没有立即执行，只是被放到`IOLoop`中，在适当的时机调用。而在`do_cb`调用的时候早就不在`try…except`块中。
    


* ####解决问题：
    那么怎么才能做到统一的处理的，可以将`try…except`部分封装起来.

    像下面这样。

        def wrap(func):
            def inner(*args, **kwargs)
                try:
                    return func(*args, **kwargs)
                except ValueException:
                    deal_with_exception()
            return inner

        def dosomething():
            def do_cb():
                raise ValueException()

            wrap(do_async(callback=wrap(do_cb)))

* ####tornado的解决方法：

    第一行：Mem
        