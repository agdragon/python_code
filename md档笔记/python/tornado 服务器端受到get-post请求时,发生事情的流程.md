# tornado 服务器端受到get/post请求时,发生事情的流程

标签（空格分隔）： tornado

---

总流程:
1. 生成`application`实例
2. 服务器监听
3. 到收到请求的时候,生成`request`对象,根据 交给 `application`查询路径映射表
4. 根据路径表生成`handler`实例.
5. 把request发送给`handler`实例.
6. `handler`实例进行处理.

详细情况如下:
(1)basehandler实例化.执行`basehandler`的`__init__()`,然后执行对应`handler`的`__init__()`
(2)当进入某个请求,比如`get()`方法, 会先执行`get_current_user()`方法.如果有这返回这个用户的信息,没有就是`None`.
(3)如果`get()`方法嵌套了修饰器, 那么就先`get`,作为参数, 传入修饰器, 先执行修饰器
(4)最后执行`get()`方法.




