import socket
import select
from model.message import message
from _pickle import loads, dumps
import sys


def process_mess(client, mes):
    if (mes.opCode == 0x0101): ## client join team ##
        print (mes.teamId)
        messend = message(0x0102, True, None)
        client.send(dumps(messend))
    elif (mes.opCode == 0x0201): ## client want question of mine ##
        Id, resource = mes.payLoad
        print ("Mine Id:", Id)
        print ("Resuorce:", resource)
        content = "Cau Hoi ABCD"
        choice = ["A", "B", "C", "D"]
        payload = content, choice
        messend = message(0x0202, True, payload)
        client.send(dumps(messend))
    elif (mes.opCode == 0x0301): ## client send answer of mine's question ##
        Id, resource, answer = mes.payLoad
        print ("Mine Id:", Id)
        print ("Resuorce:", resource)
        print ("Answer:", answer)
        messend = message(0x0302, True, None)
        client.send(dumps(messend))
    elif (mes.opCode == 0x0401): ## client buy attack ##
        print ("Team Id:", mes.teamId)
        print ("Attack:",mes.payLoad)
        messend = message(0x0402, False, "Not enough resource!")
        client.send(dumps(messend))
    elif (mes.opCode == 0x0501): ## client attack castle ##
        print ("Team Id:", mes.teamId)
        print ("Castle Id:", mes.payLoad)
        payload = "Cau Hoi Lau Dai", ["A","B","C","D"]
        messend = message(0x0502, True, payload)
        client.send(dumps(messend))
    elif (mes.opCode == 0x0601): ## client buy defend ##
        print ("Team Id:", mes.teamId)
        castleId , name = mes.payLoad
        print ("Castle Id:", castleId)
        print ("Name of Defend:", name)
        messend = message(0x0602, False, "Not enough resuorce")
        client.send(dumps(messend))
    elif (mes.opCode == 0x0701):
        Id, resource, answer = mes.payLoad
        print ("Castle Id:", Id)
        print ("Answer:", answer)
        messend = message(0x0702, False, None)
        client.send(dumps(messend))
    elif (mes.opCode == 0x0801):
        pass
    else:
        pass

list_team = []
for i in range(3):
    list_team.append([i+1, 0, 0, 0, 0])

def main():
    try:        
        host = sys.argv[1]
        port = int(sys.argv[2])
    except:
        print ("Error argv!")
        exit()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host,port))
    server.listen(10)
    server.setblocking(0)

    epoll = select.epoll()

    epoll.register(server.fileno(), select.EPOLLIN)
    try:
        connections = {}
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == server.fileno():
                    try:
                        connection, address = server.accept()
                        connection.setblocking(0)
                        epoll.register(connection.fileno(), select.EPOLLIN)
                        connections[connection.fileno()] = connection
                        connection.send(dumps(message(0x0802,None,list_team)))
                    except:
                        pass
                elif event & select.EPOLLIN:
                    try:
                        mes = loads(connections[fileno].recv(2048))
                        process_mess(connections[fileno], mes)
                        epoll.modify(fileno, select.EPOLLIN)
                    except:
                        pass
                elif event & select.EPOLLOUT:
                    pass
                elif event & select.EPOLLHUP:
                    epoll.unregister(fileno)
                    connections[fileno].close() 
                    del connections[fileno]
    finally:
        epoll.unregister(server.fileno())
        epoll.close()
        server.close()

if __name__ == '__main__':
    main()
