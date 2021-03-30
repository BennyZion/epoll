# -*- coding:utf-8 -*-

from socket import *
import json
import struct


def epoll_client(tuple_server_addr):
    # 初始化服务端主套接字
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(tuple_server_addr)

    while True:
        # 输入信息
        data_send = input('Your msg:').encode('utf8')
        # 对输入的信息计算长度，构建报头
        dict_head = {'total_size': len(data_send)}
        bytes_json_head = json.dumps(dict_head).encode('utf8')
        # 计算报头的长度
        len_head = len(bytes_json_head)
        # 对报头长度这个数据进行压缩，成为固定四个字节的二进制
        byte_len_head = struct.pack('i', len_head)
        # 发送报头长度
        client.send(byte_len_head)
        # 发送报头
        client.send(bytes_json_head)
        # 发送数据
        client.send(data_send)
        # 接收信息
        data_recv = client.recv(1024).decode('utf8')
        print("From server:", data_recv)


if __name__ == '__main__':
    epoll_client(('127.0.0.1', 8848))
