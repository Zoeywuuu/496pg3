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

# Any global variables
BUFFER = 4096




"""
The thread target function to handle the requests by a user after a socket connection is established.
Args:
    args:  any arguments to be passed to the thread
Returns:
    None
"""
def chatroom(sock):
    print("in chatroom")
    # Task1: login/register the user
    if user_name(newsock):
        newsock.send("Successfully login!".encode())

    # Task2: use a loop to handle the operations (i.e., BM, PM, EX)
    
    return

def user_name(newsock):
    try:
        username = newsock.recv(BUFFER).decode()
        print(f"{username} received.")

        password = check_user(username)
        while True:
            received_password = newsock.recv(BUFFER).decode()
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
                newsock.send("Create New User".encode())
                break
        return True

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


if __name__ == '__main__':
    # TODO: Validate input arguments
    host = ''
    port = int(sys.argv[1])
    sin = (host, port)

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

    while True:
        print(f"Waiting for connections on port {port}")

        # TODO: handle any incoming connection with UDP or TCP
        try:
            newsock, client_address = serversock.accept()
        except socket.error as e:
            print('Failed to accept the connection.')
            sys.exit()

        # TODO: initiate a thread for the connected user
        chatroom(newsock)
       





