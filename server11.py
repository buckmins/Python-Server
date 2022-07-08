
import threading 
import socket 

PORT = 1026
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
HEADER = 1024
DISCONNECT_MESSAGE = "END_CYCLE"
VITA_R = 'yes'
VITA_I = 'yes'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []
functions = []
aliases = ["Robot", "Iconet"]
aliases_iter = zip(clients,aliases)
aliases_dict = dict(aliases_iter)


def broadcast(text):
    for client in clients:
        client.send(text)
        

def handle_robot(client,addr):
    functions.append(handle_robot)
    print('ROBOT: [CONNECTED]')
    client.send('VITA'.encode(FORMAT))
    vita_robot_response = client.recv(HEADER).decode(FORMAT)
    print('Robot:'+ vita_robot_response)
    if vita_robot_response == VITA_R:
        print('vita received from robot')
        global vita_robot
        vita_robot = True
        print('vita of robot is:'+str(vita_robot))
    else:
        print('vita from robot not receivd')
        vita_robot = False
        print('vita of robot is:'+str(vita_robot))

    job_finish = client.recv(HEADER)
    print(job_finish)
    broadcast(job_finish)
    

def handle_iconet(client,addr):
    functions.append(handle_iconet)
    print('ICONET: [CONNECTED]')
    
    if vita_robot == True:
        client.send('VITA'.encode(FORMAT))
        vita_iconet_response = client.recv(HEADER).decode(FORMAT)
        print(vita_iconet_response)
    else: 
        print('Robot has not given vita')
    
    if vita_iconet_response == VITA_I:
        print('vita received from iconet')
        vita_iconet = True
        print('vita of iconet is:'+str(vita_iconet))
    else: 
        print('vita from iconet not received')
        vita_iconet = False 
        print('vita of iconet is:'+str(vita_iconet))
            
    while vita_robot and vita_iconet == True:
        client.send('LOCA'.encode(FORMAT))
        values_iconet = client.recv(HEADER)
        print(values_iconet)
        broadcast(values_iconet)
     



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"[NEW CONNECTION] {addr} connected.")
        for client in clients:
            if client == clients[0]:
                thread = threading.Thread(target = handle_robot, args=(client,addr))
            else:
                thread = threading.Thread(target = handle_iconet, args =(client,addr))
        thread.start()
       

print ('[STARTING] server is starting')
start()



