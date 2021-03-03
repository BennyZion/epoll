# -*- coding:utf-8 -*-

from socket import *
import select
import struct
import json
server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('', 8848))
server.listen(1024)

epoll_obj = select.epoll()
timeout = 10
epoll_obj.register(server.fileno(), select.EPOLLIN)

dict_fd_socket ={server.fileno():server}
print("Initial success! listening...")
while True:
    print("Waiting for connection")
    list_fd_event = epoll_obj.poll(timeout)
    if not list_fd_event:
        print('No events, retrying...')
        continue
    print('%d event(s) in event_list, start working!' %(len(list_fd_event)))
    for fd, event in list_fd_event:
        if fd == server.fileno():
            new, addr = server.accept()
            epoll_obj.register(new.fileno(), select.EPOLLIN)
            dict_fd_socket[new.fileno()] = new
        else:
            byte_len_bytes_head = dict_fd_socket[fd].recv(4)
            len_bytes_head = struct.unpack('i', byte_len_bytes_head)[0]
            json_head = dict_fd_socket[fd].recv(len_bytes_head).decode('utf8')
            dic_head = json.loads(json_head)

            data = b''
            while len(data) < dic_head['total_size']:
                data = data + dict_fd_socket[fd].recv(1024)
            if data:
                data = data.decode('utf8')
                print('Data from', dict_fd_socket[fd].getpeername(), ':'+data)
                dict_fd_socket[fd].send(data.upper().encode('utf8'))
            else:
                dict_fd_socket[fd].close()
                epoll_obj.unregister(fd)
                del dict_fd_socket[fd]
