# -*- coding: utf-8 -*-

import select
import socket
import sys

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

inputs = [server, sys.stdin]
running = True

while True:
    try:
        # 调用 select 函数，阻塞等待
        readable, writeable, exceptional = select.select(inputs, [], [])
    except select.error, e:
        break

    # 数据抵达，循环
    for sock in readable:
        # 建立连接
        if sock == server:
            conn, addr = server.accept()
            # select 监听的socket
            inputs.append(conn)
        elif sock == sys.stdin:
            junk = sys.stdin.readlines()
            running = False
        else:
            try:
                # 读取客户端连接发送的数据
                data = sock.recv(BUFFER_SIZE)
                if data:
                    sock.send(data)
                    if data.endswith('\r\n\r\n'):
                        # 移除select监听的socket
                        inputs.remove(sock)
                        sock.close()
                else:
                    # 移除select监听的socket
                    inputs.remove(sock)
                    sock.close()
            except socket.error, e:
                inputs.remove(sock)

server.close()