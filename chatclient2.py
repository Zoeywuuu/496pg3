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
from pg3lib import *


# Any global variables
BUFFER = 4096
# MESSAGE = []




"""
The thread target fuction to handle any incoming message from the server.
Args:
    None
Returns:
    None
Hint: you can use the first character of the message to distinguish different types of message
"""
def accept_messages(clientsock):
    # public_key = None
    try:
        while True:
            msg_received = clientsock.recv(BUFFER).decode()
            if msg_received.startswith("From"):
                print(msg_received)
                print(prompt, end='')
            elif msg_received.startswith('USER_LIST'):
                online_users = json.loads(msg_received[9:])
                print("\nOnline Users:", online_users)
            elif int(msg_received) == -1:
                print('The user does not exist. Failure in sending private msg.')
                print(prompt, end='')
            elif int(msg_received) == -2:
                print('Please choose another user instead of yourself.')
                print(prompt, end='')
            elif int(msg_received) == 1:
                print('Successfully sent.')
                print(prompt, end='')
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
    public_key = clientsock.recv(BUFFER)
    while True:
        # send password to server
        password = input("Please input the password:")
        password_encrypted = encrypt(password.encode(), public_key)
        clientsock.send(password_encrypted)

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
    message = input("Please type in your message to broadcast:")
    clientsock.send(message.encode())
    return True


def private(clientsock):
    print("----Enter private function-----")
    target = input("Send your private message to whom:")

    clientsock.send(target.encode())
    message = input("Type in your private message:")
    clientsock.send(message.encode())



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


