import socket
import _pickle as pickle

host = "127.0.0.1"
port = 5500

client = socket.socket()
client.connect((host, port))

def main():
    global list_team, team_id, check, root_frame, mainframe
    while check:
        mes = pickle.loads(client.recv(2048))
        if (mes.opcode == 0x0102):
            #do something
            mainframe = main_frame(main)
            mainframe.mainloop()
        elif (mes.opcode == 0x0202):
            #do something
            pass
        elif (mes.opcode == 0x0302):
            #do something
            pass
        elif (mes.opcode == 0x0402):
            #do something
            pass
        elif (mes.opcode == 0x0502):
            #do something
            pass
        elif (mes.opcode == 0x0602):
            #do something
            pass
        elif (mes.opcode == 0x0702):
            #do something
            pass
        elif (mes.opcode == 0x0802):
            #do something
            pass
        else:
            #do something
            pass

if __name__ == '__main__':
    main()