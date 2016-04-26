启动测试程序:
---------------

start a worker:
    celery -A tasks worker --loglevel=info -n new
    如果报错:
        "Running a worker with superuser privileges when the worker accepts messages serialized with pickle is a very bad idea!"
    则执行:
        'export C_FORCE_ROOT="true" '

and start tornado server.    
    python test.py


该模块的核心思想:
---------------

    1：判断是否需要执行回调，如果需要执行回调，先把回调函数加future的回调函数列表中。
    2：调用celery的delay函数
    3：等待celery执行的结果。同时将处理等待celery执行的结果的函数通过add_callback加到IOLoop.instance中去。