# -*- coding:utf-8 -*-

from socket import *
import json
import struct

socket = socket(AF_INET, SOCK_STREAM)
tuple_server_addr = ('127.0.0.1', 8848)
socket.connect(tuple_server_addr)

while True:
    data_send = input('Your msg:').encode('utf8')
    dict_head = {'total_size': len(data_send)}
    bytes_json_head = json.dumps(dict_head).encode('utf8')
    len_head = len(bytes_json_head)
    byte_len_head = struct.pack('i',len_head)
    socket.send(byte_len_head)
    socket.send(bytes_json_head)
    socket.send(data_send)
    data_recv = socket.recv(1024).decode('utf8')
    print("From server:", data_recv)



