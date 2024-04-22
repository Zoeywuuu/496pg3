# 496pg3

There are 4 python files in this folder:

chatserver.py and chatclient.py achieve BM, PM, EXIT functions.
chatserver2.py and chatclient2.py achieve BM, PM, EXIT, CH and encrypt password functions.



 How to test our program on student machine? Please follow the instruction. 
 First, upload all the files to students machines by command ""scp * username@student00.ischool.illinois.edu:"
 
To test main parts, please run the chatserver.py on student machine 01,
and run the chatclient.py in other student machines.

******LOGIN PROCESS******
Type in "python3 chatserver.py portnumber" in terminal and "python3 chatserver.py machinename portnumber".
For log in process, if the old user, the output should be.

in server side：
in chatroom
Waiting for connections on port 41001
aaa received.
conn established with username aaa
Wait for operation from client.

in client side：
-----enter username function-------
Please input the username:aaa
Please input the password:bbb
ack: Match successfully!
response:Successfully login!
Please type in your operation (BM/PM/EX):

if the new user：
same as in server side but differs in client side
-----enter username function-------
in  client side：
Please input the username:rrr
Please input the password:ttt
ack: Create New User
response:Successfully login!
Please type in your operation (BM/PM/EX):

******BM FUNCTION******
The expected output for the BM function 

in server side:
Operation received: BM.
Wait for operation from client.

in client side who send the BM msg:
Please type in your operation (BM/PM/EX):
BM
Please type in your message to broadcast:QQQ
Please type in your operation (BM/PM/EX):

in client who receives the BM msg:
Please type in your operation (BM/PM/EX):
From aaa (broadcast message): QQQ
Please type in your operation (BM/PM/EX):

******PM FUNCTION******
The expected output for the PM function 

server side:
-----enter private function------
USER_LIST["rrr", "aaa"]
Successfully sent.
Wait for operation from client.

client who want to send PM msg:
----Enter private function-----
Send your private message to whom:
Online Users: ['rrr', 'aaa']
rrr
Type in your private message:uiuiuiuiuiui
Please type in your operation (BM/PM/EX):
Successfully sent.
Please type in your operation (BM/PM/EX):

client who receives the PM msg:
From aaa (private message): uiuiuiuiuiui

if the user not online or is the sender client self, will print wrong messages like:
in server side:
The user does not exist./Please choose another user instead of the client self.

in sender client side:
The user does not exist. Failure in sending private msg./
Please choose another user instead of yourself.

******EX FUNCTION******
The expected output for the EX function 

in server side:
Wait for operation from client.
Operation received: EX.
Closing the thread...

in client side:
Please type in your operation (BM/PM/EX):
EX
Closing the thread...


To test extra credits, please run the chatserver2.py on student machine 01,
and run the chatclient2.py in other student machines

 Attention: please create new users for test CH function and please wait for a while to enter CH

******CH FUNCTION******

client side:
start printing history

2024-04-22 13:30:24 BM From aaa (broadcast message): test
2024-04-22 13:30:48 BM From aaa (broadcast message): test2
2024-04-22 13:35:00 BM From aaa(broadcast message): 33333

-----

server side:

Wait for operation from client.
Operation received: CH.


