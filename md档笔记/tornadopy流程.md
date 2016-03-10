# tornadopy源码分析

标签（空格分隔）： python

---

- `server = Server()`
- `parse_command()`
- `load_urls()`
- `load_application(application)`
    1. `_patch_httpserver()`
    2. `locale.load_translations()`
    3. `_install_application()`
        1. 设置`tornado_conf`
        2. `Application()`
            1. `middleware_fac = Manager()`
            2. `middleware_fac.register_all()`
            3. `middleware_fac.run_init()`

- `load_httpserver()`
- `ioloop = tornado.ioloop.IOLoop.instance()`
- `ioloop.start()`


