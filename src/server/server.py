import socket
import select
from _pickle import loads, dumps
import sys, os
from message import message
from controller.controller import controller
from threading import Thread
from model.resource import RESOURCES
from model.interval import VALUE
from time import sleep
from model.scheduler import check_data
from threading import Timer

is_finished = False

control = controller()

timer = check_data(control.teams, control.fields, control.castles, True)


def setFinish():
    global is_finished
    is_finished = False

timer_game = Timer(4 * 60 * 60.0, setFinish).start()

def multikeysort(items, columns):
    from operator import itemgetter
    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else
                  (itemgetter(col.strip()), 1)) for col in columns]
    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)

def updateData(init=True):
    global control

    while init:
        sleep(1)
        for field in control.fields:
            for resource in RESOURCES[:2]:
                teams_have_resource = field.reduce_time(resource)

                for solver in teams_have_resource:
                    control.teams[solver-1].add_resource(resource, VALUE[resource])

        for castle in control.castles:
            resource = RESOURCES[3]
            if castle.owner_id != None:
                if castle.reduce_gold_delay():
                    control.teams[castle.owner_id-1].add_resource(resource, VALUE[resource])

serverData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverData.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverData.bind(("0.0.0.0",8080))
serverData.listen(10)
list_client = []
def listen():
    while True:
        connection, address = serverData.accept()
        list_client.append(connection)

def sendData():
    global is_finished

    while True:
        sleep(1)

        if is_finished:
            # Send data to client
            winner = sorted(control.teams, lambda team: (team.resources['gold'],
                                                         team.resources['iron'],
                                                         team.resources['stone'],
                                                         team.resources['wood']))


            print('Winner is {}'.format(winner.name))

            quit()

        for client in list_client:
            try:
                mes = message(0x0902, None, control.getData())
                client.send(dumps(mes))
            except:
                list_client.remove(client)

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
        if result == "is_solved":
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
            result = control.buy_attack(teamId, itemname)
        except:
            result = "Error"
        if result == True:
            messend = message(0x0402, True, "Buy Complete!")
        elif result == "had_it":
            messend = message(0x0402, False, "Sorry! You had it!")
        elif result == 'you_had_best':
            messend = message(0x0402, False, "Sorry! You had best attack!")
        elif result == 'not_enough':
            messend = message(0x0402, False, "Sorry! Not enough resources!")
        elif result == False:
            messend = message(0x0402, False, "Can not buy! Please try again!")
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
            result = control.team_attack(teamId, castleId)
        except:
            result = "Error!"
        if result == "blocked":
            messend = message(0x0502, False, "Castle is blocked!")
        elif result == "empty_castle" or result == True:
            try:
                quesId = control.get_questionid_castle(castleId)
                payload = control.get_question_by_id(quesId)
                messend = message(0x0502, True, payload)
            except:
                messend = message(0x0502, False, "Error! Please try again!")
        elif result == "our_castle":
            messend = message(0x0502, False, "Can not attack our castle!")
        elif result == False:
            messend = message(0x0502, False, "Attack false!")
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
            result = control.buy_defense(teamId, castleId, itemname)
        except:
            result = "Error"
        if result == True:
            messend = message(0x0602, True, "Buy Complete!")
        elif result == "you_had_best":
            messend = message(0x0602, False, "Sorry! You had the best defence!")
        elif result == "not_owner":
            messend = message(0x0602, False, "Sorry! You must owned castle!")
        elif result == 'not_enough':
            messend = message(0x0602, False, "Not enough resources")
        elif result == False:
            messend = message(0x0602, False, "Sorry cannot buy! Please try again!")
        else:
            messend = message(0x0602, False, "Error! Please try again!")
        try:
            client.send(dumps(messend))
        except:
            pass
    elif (mes.opCode == 0x0701): ## client answer question of castle ##
        teamId = mes.teamId
        castleId, resource, answer = mes.payLoad
        try:
            result = control.check_answer_castle(castleId, answer)
        except:
            result = "Error"
        if result == True:
            try:
                control.answer_castles_success(teamId, castleId)
                messend = message(0x0702, True, None)
            except:
                messend = message(0x0702, False, "Error! Please try again!")
        elif result == False:
            messend = message(0x0702, False, "Answer Incorrect!")
        else:
            messend = message(0x0702, False, "Error! Please try again!")
        try:
            client.send(dumps(messend))
        except:
            pass
    elif (mes.opCode == 0x0801):
        pass
    else:
        pass

def main():
    host = "0.0.0.0"
    port = 5500
    # thread1 = Thread(target = updateData,)
    # thread1.start()
    thread2 = Thread(target = listen,)
    thread2.start()
    thread3 = Thread(target = sendData,)
    thread3.start()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host,port))
    server.listen(10)
    server.setblocking(0)
    epoll = select.epoll()
    epoll.register(server.fileno(), select.EPOLLIN)
    print ("Server started!")
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
                        connection.send(dumps(message(0x0802,None,control.getData()[0])))
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
