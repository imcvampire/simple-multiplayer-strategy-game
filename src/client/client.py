import socket
from tkinter import *
from _pickle import loads, dumps
from model.message import message
from model.startFrame import startFrame

host = "127.0.0.1"
port = 5500

def main():
    root = Tk()
    client = socket.socket()
    client.settimeout(2.0)
    client.connect((host, port))
    mesrcv = loads(client.recv(2048))
    if mesrcv.opCode == 0x0802:
        list_team = mesrcv.payLoad
        frame = startFrame(client, root, list_team)
        frame.mainLoop()
    else:
        pass
    client.close() 

if __name__ == '__main__':
    main()