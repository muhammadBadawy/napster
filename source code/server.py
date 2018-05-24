import sys
import socket
from thread import *
import functions

host = 'localhost'
port = 5323

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #For only Unix and Linux

try:
    s.bind((host, port))
except socket.error, msg:
    print '# Failed with Error : ' + str(msg[0]) + ' Saying : ' + msg[1]
    sys.exit()
s.listen(10)

print 'Listening for connections'

onlinePeers = []
users = {}


def clientthread(conn, addr):
    conn.send(
        'Service Started. Choose an option Useing Uppercase letter\n #(R)egister\n #(U)pload files\n #(S)earch for a file\n #(E)xit')
    onlinePeers.append(addr[0])
    while True:
        data = conn.recv(1024)

        if not data:
            continue
        elif data.split('\n')[0] == 'REGISTER':
            functions.register(conn, addr, data.split('\n')[1], str(addr[1]))
            # functions.register(conn, addr, "client" + str(addr[1]))
        elif data.split('\n')[0] == 'SHARE_FILES':
            functions.share(conn, addr, data.split('\n')[1], str(addr[1]))
        elif data.split('\n')[0] == 'SEARCH':
            functions.search(conn, addr, data.split('\n')[1], onlinePeers)


    onlinePeers.remove(addr[0])
    conn.close()


while True:
    conn, addr = s.accept()
    print 'Got connection From ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread, (conn, addr))

s.close()
