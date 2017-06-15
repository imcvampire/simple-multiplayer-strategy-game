import socket
import select
from _pickle import loads, dumps
import sys, os
from model.message import message
from controller.controller import controller

control = controller()

def process_mess(client, mes):
    if (mes.opCode == 0x0101): ## client join team ##
        teamId = mes.teamId
        try:
            result = control.join_team("player", teamId)
        except:
            result = "Error"
        if result == True:
            messend = message(0x0102, True, None)
        elif result == "max_players":
            messend = message(0x0102, False, "The team is max player!")
        elif result == False:
            messend = message(0x0102, False, "Team id is not exist!")
        else:
            messend = message(0x0102, False, "Error! Please try again!")
        try:
            client.send(dumps(messend))
        except:
            pass
    elif (mes.opCode == 0x0201): ## client want question of mine ##
        mineId, resource = mes.payLoad
        try:
            content, choice = control.get_question_mine(mineId, resource)
        except:
            content, choice = None, None
        if content == None:
            messend = message(0x0202, False, "Error! Please try again!")
        else:
            payload = content, choice
            messend = message(0x0202, True, payload)
        try:
            client.send(dumps(messend))
        except:
            pass
    elif (mes.opCode == 0x0301): ## client send answer of mine's question ##
        teamId = mes.teamId
        mineId, resource, answer = mes.payLoad
        try:
            result = control.check_answer_mine(mineId, resource, teamId, answer)
        except:
            result = "Error"
        if result == "is_sloved":
            messend = message(0x0302, False, "You sloved")
        elif result == True:
            messend = message(0x0302, True, None)
        elif result == False:
            messend = message(0x0302, False, "Answer Incorrect")
        else:
            messend = message(0x0302, False, "Error! Please try again!")
        try:
            client.send(dumps(messend))
        except:
            pass
    elif (mes.opCode == 0x0401): ## client buy attack ##
        teamId = mes.teamId
        itemname = mes.payLoad
        try:
            result = control.buy_item(teamId, itemname, "attack")
        except:
            result = "Error"
        if result == True:
            messend = message(0x0402, True, "Buy Complete!")
        elif result == False:
            messend = message(0x0402, False, "Cannot buy!")
        else:
            messend = message(0x0402, False, "Error! Please try again!")
        try:
            client.send(dumps(messend))
        except:
            pass
    elif (mes.opCode == 0x0501): ## client attack castle ##
        teamId = mes.teamId
        castleId = mes.payLoad
        try:
            result = control.check_castle(teamId, castleId)
        except:
            result = "Error!"
        if result == "blocked":
            messend = message(0x0502, False, "Castle is blocked!")
        elif result == "empty_castle":
            try:
                quesId = control.get_questionid_castle(castleId)
                payload = control.get_question_by_id(quesId)
                messend = message(0x0502, True, payload)
            except:
                messend = message(0x0502, False, "Error! Please try again!")
        elif result == "our_castle":
            messend = message(0x0502, False, "Can not attack our castle!")
        elif result == "attack":
            try:
                att = control.attack_castle(teamId, castleId)
                if att == True:
                    quesId = control.get_questionid_castle(castleId)
                    payload = control.get_question_by_id(quesId)
                    messend = message(0x0502, True, payload)
                elif att == False:
                    messend = message(0x0502, False, "Damage attack not enough!")
                else:
                    messend = message(0x0502, False, "Error! Please try again!")
            except:
                messend = message(0x0502, False, "Error! Please try again!")
        else:
            messend = message(0x0502, False, "Error! Please try again!")
        try:
            client.send(dumps(messend))
        except:
            pass
    elif (mes.opCode == 0x0601): ## client buy defend ##
        teamId = mes.teamId
        castleId , itemname = mes.payLoad
        try:
            result = control.set_defense(teamId, castleId, itemname)
        except:
            result = "Error"
        if result == True:
            messend = message(0x0402, True, "Buy Complete!")
        elif result == "cant_set_defense":
            messend = message(0x0402, False, "Cannot buy defend!")
        elif result == False:
            messend = message(0x0402, False, "Cannot set defend")
        else:
            messend = message(0x0402, False, "Error! Please try again!")
        try:
            client.send(dumps(messend))
        except:
            pass
    elif (mes.opCode == 0x0701):
        teamId = mes.teamId
        castleId, resource, answer = mes.payLoad
        try:
            quesId = control.get_questionid_castle(castleId)
            result = check_answer(answer, quesId)
            if result == True:
                control.answer_castles_success(teamId, castleId)
                messend = message(0x0702, True, None)
            else:
                messend = message(0x0702, False, "Answer Incorrect!")
        except:
            messend = message(0x0402, False, "Error! Please try again!")
        try:
            client.send(dumps(messend))
        except:
            pass
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
