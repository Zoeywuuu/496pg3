# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and Netid of each member:
# Member 1: 
# Member 2: 
# Member 3: 


# Note: 
# This starter code is optional. Feel free to develop your own solution. 

# Import any necessary libraries below
import socket
import threading
import sys, os, struct

# Any global variables
BUFFER = 4096




"""
The thread target fuction to handle the requests by a user after a socket connection is established.
Args:
    args:  any arguments to be passed to the thread
Returns:
    None
"""
def chatroom(sock):
    print("in chatroom")
    # Task1: login/register the user
   

    # Task2: use a loop to handle the operations (i.e., BM, PM, EX)
    
    return





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
       





