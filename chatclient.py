# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and Netid of each member:
# Member 1: Chloe Cai (keyucai2)
# Member 2: Zeyu Wu (zeyuwu5)



# Note: 
# This starter code is optional. Feel free to develop your own solution. 


# Import any necessary libraries below
import socket
import threading
import sys, os, struct
import json

# Any global variables
BUFFER =  4096




"""
The thread target fuction to handle any incoming message from the server.
Args:
    None
Returns:
    None
Hint: you can use the first character of the message to distinguish different types of message
"""
def accept_messages(clientsock):
    global MESSAGE
    try:
        while True:
            msg_received = clientsock.recv(BUFFER).decode()
            print(msg_received)
            if msg_received.startswith("From"):
                print(msg_received)
                print(prompt, end='')
            elif isinstance(msg_received, list):
                MESSAGE.append(msg_received)
                print(MESSAGE)
                # print('3')
                # if msg_type == "BM":
                #     print("Broadcast Message:", message)
                # elif msg_type == "PM":
                #     print("Private Message:", message)
                # elif msg_type == "EX":
                #     print("Server has closed the connection.")
                #     break
            else:
                continue
    except Exception as e:
        print("Error in accept_messages:", e)
    finally:
        clientsock.close()
    return True


def username(clientsock):
    print("-----enter username funtion-------")
    # send username to server
    username = input("Please input the username:")
    clientsock.send(username.encode())
    while True:
        # send password to server
        password = input("Please input the password:")
        clientsock.send(password.encode())

        # receive the response from server
        ack = clientsock.recv(BUFFER).decode()
        print(f"ack: {ack}")
        if ack == "Wrong Password! Please type in your password again":
            continue
        else:
            response = clientsock.recv(BUFFER).decode()
            print(f"response:{response}")
            break

def broadcast(clientsock):
    # ack = clientsock.recv(BUFFER).decode()
    # print(ack)
    message = input("Please type in your message to broadcast:")
    clientsock.send(message.encode())
    # confirmation = clientsock.recv(BUFFER).decode()
    # print(confirmation)
    return True

def private(clientsock):
    MESSAGE = []
    print("----Enter private function-----")
    print(MESSAGE)
    # print('2')
    target = input("Send your private message to whom:")
    clientsock.send(target.encode())
    message = input("Type in your private message:")
    clientsock.send(message.encode())
    # confirmation = clientsock.recv(BUFFER).decode()
    # print(confirmation)


if __name__ == '__main__': 
    # TODO: Validate input arguments
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    host = socket.gethostbyname(hostname)
    sin = (host, port)

    # TODO: create a socket with UDP or TCP, and connect to the server
    try:
        clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print(f'Failed to create socket. Error Code : {str(msg[0])}\n Message: {msg[1]}')
        sys.exit()
    
    try:
        clientsock.connect(sin)
    except socket.error as e:
        print('Failed to connect to the server.')
        sys.exit()
    
    # TODO: Send username to the server and login/register the user
    username(clientsock)


    # TODO: initiate a thread for receiving message
    recv_thread = threading.Thread(target = accept_messages, args = (clientsock,))
    recv_thread.start()


    # TODO: use a loop to handle the operations (i.e., BM, PM, EX)
    while True:
        prompt = 'Please type in your operation (BM/PM/EX):\n'
        operation = input(prompt)

        clientsock.send(operation.encode())
        if operation == 'EX':
            print('Closing the thread...')
            clientsock.close()
            break
        elif operation == 'BM':
            broadcast(clientsock)
        elif operation == 'PM':
            private(clientsock)
        else:
            print('Wrong operation. Please reenter.')

    clientsock.close()
    sys.exit()


