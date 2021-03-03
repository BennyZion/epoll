# -*- coding:utf-8 -*-

from socket import *
socket = socket(AF_INET, SOCK_STREAM)
tuple_server_addr = ('127.0.0.1', 8848)
socket.connect(tuple_server_addr)

while True:
    data_send = input('Your msg:')
    socket.send(data_send.encode('utf8'))
    data_recv = socket.recv(1024).decode('utf8')
    print("From server:", data_recv)



