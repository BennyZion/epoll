# -*- coding:utf-8 -*-

from socket import *
import select
import struct
import json


def epoll_server(tuple_ip_port, max_listen, epoll_time_out):
    # 初始化主句柄，用来监听连接
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(tuple_ip_port)
    server.listen(max_listen)
    # 讲主套接字设置为非阻塞
    server.setblocking(flag=False)
    # 初始化epoll对象
    epoll_obj = select.epoll()
    # 将主句柄的文件描述符以及事件注册进epoll对象
    epoll_obj.register(server.fileno(), select.EPOLLIN)
    # 设计一个 字典用来存储fd和socket的映射
    dict_fd_socket = {server.fileno(): server}
    print("Initial success! listening...")
    # 定义循环，接收事件
    while True:
        print("Waiting for connection")
        list_fd_event = epoll_obj.poll(epoll_time_out)
        # fd_event用来存储epoll返回的fd,event元组
        if not list_fd_event:
            print('No events, retrying...')
            continue
        print('%d event(s) in event_list, start working!' % (len(list_fd_event)))
        # 遍历fd_event列表，处理其中的事件
        for fd, event in list_fd_event:
            # 如果是主套接字，那么接收连接请求，并注册到epoll对象中
            if fd == server.fileno():
                new, addr = server.accept()
                epoll_obj.register(new.fileno(), select.EPOLLIN)
                dict_fd_socket[new.fileno()] = new
            # 处理非主套接字的事件
            else:
                # 首先接收四字节的报文，这四个字节是报头长度的压缩后的二进制形式
                byte_len_bytes_head = dict_fd_socket[fd].recv(4)
                # 对四个字节进行解码，得到报头长度
                len_bytes_head = struct.unpack('i', byte_len_bytes_head)[0]
                # 使用报头长度去接收信息，得到报头的二进制形式，再进行解码得到json压缩的字符串形式
                json_head = dict_fd_socket[fd].recv(len_bytes_head).decode('utf8')
                # 对json字符串进行加载得到字典
                dic_head = json.loads(json_head)
                # 初始化数据为二进制形式
                data = b''
                # 开始循环接收数据直到接收数据等于报头中执行的大小
                while len(data) < dic_head['total_size']:
                    data = data + dict_fd_socket[fd].recv(1024)
                # 如果存在数据则进行处理
                if data:
                    data = data.decode('utf8')
                    print('Data from', dict_fd_socket[fd].getpeername(), ':' + data)
                    dict_fd_socket[fd].send(data.upper().encode('utf8'))
                # 如果不存在数据则断开连接
                else:
                    dict_fd_socket[fd].close()
                    epoll_obj.unregister(fd)
                    del dict_fd_socket[fd]
if __name__ == '__main__':
    epoll_server(('', 8848), 1024, 10)