# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and Netid of each member:
# Member 1: Chloe Cai (keyucai2)
# Member 2: Zeyu Wu (zeyuwu5)


# Note: 
# This starter code is optional. Feel free to develop your own solution. 

# Import any necessary libraries below
# import logging
import socket
import threading
import sys, os, struct
import json
import time

from pg3lib import *

# Any global variables
BUFFER = 4096
CHAT_HISTORY_DIR = "chat_history"




"""
The thread target function to handle the requests by a user after a socket connection is established.
Args:
    args:  any arguments to be passed to the thread
Returns:
    None
"""
def chatroom(newsock, lst):
    print("in chatroom")
    # Task1: login/register the user
    username = handle_login(newsock)
    newsock.send("Successfully login!".encode())
    lst[username] = newsock

    # Task2: use a loop to handle the operations (i.e., BM, PM, EX)
    while True:
        print("Wait for operation from client.")
        operation = newsock.recv(4).decode()
        print(f'Operation received: {operation}.')
        if operation == 'EX':
            lst.pop(username)
            print('Closing the thread...')
            newsock.close()
            break
        elif operation == 'BM':
            broadcast(newsock, username, lst)
            # continue
        elif operation == 'PM':
            private(newsock, username, lst)
            # continue
        elif operation == 'CH':
            history(newsock, username)
        else:
            print('Wrong operation.')
            # continue
    return


def broadcast(newsock, username, lst):
    # newsock.send("Will broadcast your message to all online users.".encode())
    message = newsock.recv(BUFFER).decode()
    msg = f"From {username} (broadcast message): {message}"
    timestamp = time.time()
    write_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp)))
    write_msg = str(write_time + ' BM ' + msg)
    write_history(username, write_msg)
    for clientsock in lst.values():
        if clientsock != newsock:
            clientsock.send(msg.encode())
    # newsock.send("Finish broadcasting message.".encode())


def private(newsock, username, lst):
    print("-----enter private function------")
    online_users = json.dumps(list(lst.keys()))
    online_clients = 'USER_LIST' + online_users
    print(online_clients)

    newsock.send(online_clients.encode())
    target = newsock.recv(BUFFER).decode()

    message = newsock.recv(BUFFER).decode()
    msg = f"From {username} (private message): {message}"
    if target in lst.keys():
        target_sock = lst[target]
        if target_sock != newsock:
            target_sock.send(msg.encode())
            ack = b'1'
            print('Successfully sent.')
            timestamp = time.time()
            write_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp)))
            print(write_time)
            write_msg = str(write_time + 'PM' + msg + 'to' + target)
            print(write_msg)
            write_history(username, write_msg)
        else:
            ack = b'-2'
            print('Please choose another user instead of the client self.')
    else:
        ack = b'-1'
        print('The user does not exist.')
    newsock.send(ack)


def handle_login(newsock):
    try:
        username = newsock.recv(BUFFER).decode()
        print(f"{username} received.")
        public_key = getPubKey()
        newsock.send(public_key)

        password = check_user(username)
        while True:
            received_encrypted_password = newsock.recv(BUFFER)
            received_password = decrypt(received_encrypted_password).decode()
            # print(received_password)
            # old user
            if password:
                # wrong password
                if received_password != password:
                    newsock.send("Wrong Password! Please type in your password again".encode())
                # password match
                else:    
                    newsock.send("Match successfully!".encode())
                    break
            # new user
            else:
                with open("user_file.txt", 'a') as f:
                    f.write(f"{username}:{received_password}\n")
                chat_history_file = os.path.join(CHAT_HISTORY_DIR, f"{username}.chat.txt")
                with open(chat_history_file,'a') as f2:
                    f2.write(f"*** chat history of {username} ***\n")
                newsock.send("Create New User".encode())
                break
        print(f"conn established with username {username}")
        return username

    except Exception as e:
        print("Error during name function:", e)
        return False


def check_user(username):
    with open("user_file.txt", "r") as f:
        for line in f:
            exist_username, password = line.strip().split(':')
            if exist_username == username:
                return password
    return None


def history(newsock,username):
    try:
        chat_history_file = os.path.join(CHAT_HISTORY_DIR, f"{username}.chat.txt")
        # print(chat_history_file)
        if os.path.exists(chat_history_file):
            with open(chat_history_file, 'r') as f:
                chat_history = f.readlines()
                # logging.info("start sending history")
                for line in chat_history:
                    # print(line)
                    # logging.info(line)
                    newsock.send(line.encode())
                # logging.info("end sending history")
        newsock.send("&&& History_End &&&".encode())


    except Exception as e:
        print("Error sending history:", e)




def write_history(username, write_msg):
    chat_history_file = os.path.join(CHAT_HISTORY_DIR, f"{username}.chat.txt")
    if os.path.exists(chat_history_file):
        # print('qqqqq')
        with open(chat_history_file, 'a') as f:
            f.write(f"{write_msg}\n")
    else:
        print('222No chat history existed.')



if __name__ == '__main__':
    # TODO: Validate input arguments
    host = ''
    port = int(sys.argv[1])
    sin = (host, port)
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # TODO: create a socket in UDP or TCP
    try:
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()
    
    # TODO: Bind the socket to address
    try:
        serversock.bind(sin)
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    try:
        serversock.listen()
    except socket.error as e:
        print('Failed to listen.')
        sys.exit()

    lst = {}

    while True:
        print(f"Waiting for connections on port {port}")

        # TODO: handle any incoming connection with UDP or TCP
        try:
            newsock, client_address = serversock.accept()
        except socket.error as e:
            print('Failed to accept the connection.')
            sys.exit()

        # TODO: initiate a thread for the connected user
        t = threading.Thread(target = chatroom, args=(newsock, lst))
        t.start()
        # print(f"start a new thread to handle request from {newsock}")
        
       





