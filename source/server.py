import time

import waysegment
import labyrint
import player

import socket
import select

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("www.kernel.org",80))
    ip_addr = s.getsockname()[0]
    s.close()
except:
    ip_addr = "localhost"

connect_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_sock.listen(10)
print "Server is online. This is my address:"
print ip_addr + " " + str(connect_sock.getsockname()[1])

#client, addr = connect_sock.accept()
#print 'Connected with ' + addr[0] + ':' + str(addr[1])

#data = client.recv(1024)
#print data
#client.sendall(data)
 
#client.close()
#connect_sock.close()




wait_list = [connect_sock]

players = []

def delete_player(player):
    wait_list.remove(player)
    players.remove(player)
    print 'Player disconnected'


def add_player():

    global wait_list, players
    global connect_sock
    client_sock, addr = connect_sock.accept()
    print 'New player connected: ' + addr[0] + ':' + str(addr[1])

    new_player = player.Player()
    new_player.ID = len(players)
    new_player.connect_to_client(client_sock)

    wait_list.append(new_player)
    players.append(new_player)

    pos_str = "0;0;0"
    lab_str = labyrint.serialize()
    send_str = str(new_player.ID) + "-" + pos_str + "-" + lab_str
    new_player.connection.sendall(send_str)

while True:
    start_time = time.time()

    read_ready, write_ready, exception_ready = select.select(wait_list, [], wait_list)

    print read_ready
    print write_ready
    print exception_ready
    for s in read_ready:
        print "read"
        if s == connect_sock:
            add_player()
        else:
            data = s.connection.recv(1024)
            print data
            if len(data) == 0: # end of file reached
                delete_player(s)
            #s.sendall(data)
    for s in write_ready:
        print "write"
    for s in exception_ready:
        print "exception"


    end_time = time.time()
    print "Time = " + str((end_time - start_time) * 1000) + " ms"
    time.sleep(0.001)
