# tornado

标签（空格分隔）： tornado

---

- tornado启动main函数
```
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
```
- 详细分解`main()`:
```
def main():
    ##下面这行是解析命令行参数，不多说
    tornado.options.parse_command_line()

    ##这行有意思了，构造一个httpserver，其实大部分都是继承至tcpserver，注意参数Application()是个对象，而且是个可调用的对象，它里面有个方法__call__可是起了核心作用
    http_server = tornado.httpserver.HTTPServer(Application())

    ##这行做的事可多了，后面详解
    http_server.listen(options.port)

    ##这行就是构造事件或者说handler的循环队列，并执行之，暂不详解
    tornado.ioloop.IOLoop.instance().start()
```
- `http_server.listen(options.port)`详解:
从tcpserver中看看他做了什么事哈：
```
def listen(self, port, address=""):
    #调用netutil中的bind_socket，返回的是绑定的所有(IP,port)地址的socket#
    sockets = bind_sockets(port, address=address)
        
    #自身的add_sockets方法中调用了netutil中的add_accept_handler#
    self.add_sockets(sockets)
```

    看看add_sockets干了什么：
```
def add_sockets(self, sockets):
    if self.io_loop is None:
        self.io_loop = IOLoop.current()
    for sock in sockets:
        self._sockets[sock.fileno()] = sock
     
        #记住这里回调的是_handle_connection，是处理请求的核心，稍后还会回头看他#
        add_accept_handler(sock,self._handle_connection,io_loop=self.io_loop)

```
    看看add_accept_handler做了什么：
```
def add_accept_handler(sock, callback, io_loop=None):
    if io_loop is None:
        io_loop = IOLoop.current()

    def accept_handler(fd, events):
        while True:
            try:
                connection, address = sock.accept()
            except socket.error as e:
                if e.args[0] == errno.ECONNABORTED:
                    continue
                raise
            callback(connection, address)
    io_loop.add_handler(sock, accept_handler, IOLoop.READ)
```
看懂了吧，就是把`callback`，也就是`_handle_connection`这个回调的`handler`加到`ioloop`的`_callback`队列中
    `io_loop.add_handler(sock.fileno(), accept_handler, IOLoop.READ)`

    看看ioloop.add_handler函数干了啥:
```
def add_handler(self, fd, handler, events):
    self._handlers[fd] = stack_context.wrap(handler)
    self._impl.register(fd, events | self.ERROR)
```
之后就由ioloop.start内的循环处理事件或者说handler了

- `handle_connection`响应请求开始:
这个函数位于tcpserver中：
```
def _handle_connection(self, connection, address):
    if self.ssl_options is not None:
        assert ssl, "Python 2.6+ and OpenSSL required for SSL"
        try:
            connection = ssl_wrap_socket(connection,
                            self.ssl_options,server_side=True,                             do_handshake_on_connect=False)
        except ssl.SSLError as err:
            if err.args[0] == ssl.SSL_ERROR_EOF:
                return connection.close()
            else:
                raise
        except socket.error as err:
            if err.args[0] in (errno.ECONNABORTED, errno.EINVAL):
                return connection.close()
            else:
                raise
    try:
        if self.ssl_options is not None:
            stream = SSLIOStream(connection, io_loop=self.io_loop, max_buffer_size=self.max_buffer_size)
        else:
            stream = IOStream(connection, io_loop=self.io_loop, max_buffer_size=self.max_buffer_size)
        self.handle_stream(stream, address)
    except Exception:
        app_log.error("Error in connection callback", exc_info=True)
```
重要的也就是实例化了`iostream`对象，这个对象专门负责读写数据。然后是调用`httpserver`重写的handle_stream方法,将`stream`交给`HTTPConnection`处理，注意这里的`request_callback`是`Application`对象

看看`handle_stream`函数:
```
def handle_stream(self, stream, address):
    HTTPConnection(stream, address, self.request_callback,self.no_keep_alive, self.xheaders, self.protocol)
```

之后就到`HTTPConnection`初始化部分，核心就是`_on_headers`方法与`read_until`:
```
def __init__(self, stream, address, request_callback, no_keep_alive=False,xheaders=False, protocol=None):
    self._header_callback = stack_context.wrap(self._on_headers)
    self.stream.set_close_callback(self._on_connection_close)

    #read_until可以暂时简单看作将数据读给_on_headers方法
    self.stream.read_until(b"\r\n\r\n", self._header_callback)
```
 再来看`_on_headers`函数:
```
 def _on_headers(self, data):
    try:
        data = native_str(data.decode('latin1'))
        eol = data.find("\r\n")
        start_line = data[:eol]
        try:
            method, uri, version = start_line.split(" ")
        except ValueError:
            raise _BadRequestException("Malformed HTTP request line")
        if not version.startswith("HTTP/"):
            raise _BadRequestException("Malformed HTTP version in HTTP Request-Line")
        try:
            headers = httputil.HTTPHeaders.parse(data[eol:])
        except ValueError:
            # Probably from split() if there was no ':' in the line
            raise _BadRequestException("Malformed HTTP headers")

        # HTTPRequest wants an IP, not a full socket address
        if self.address_family in (socket.AF_INET, socket.AF_INET6):
            remote_ip = self.address[0]
        else:
            # Unix (or other) socket; fake the remote address
            remote_ip = '0.0.0.0'

        self._request = HTTPRequest(connection=self, method=method, uri=uri, version=version,headers=headers, remote_ip=remote_ip, protocol=self.protocol)

        content_length = headers.get("Content-Length")
        if content_length:
            content_length = int(content_length)
            if content_length > self.stream.max_buffer_size:
                raise _BadRequestException("Content-Length too long")
            if headers.get("Expect") == "100-continue":
                self.stream.write(b"HTTP/1.1 100 (Continue)\r\n\r\n")
            self.stream.read_bytes(content_length, self._on_request_body)
            return

        self.request_callback(self._request)
    except _BadRequestException as e:
        gen_log.info("Malformed HTTP request from %s: %s",self.address[0], e)
        self.close()
        return
```


