# import socket module
from socket import *
import sys
import threading

HOST = '0.0.0.0'
PORT = 80

def work(connectionSocket, addr):
    try:
        message = connectionSocket.recv(2048)
        print(message.decode())
        filename =  message.split()[1]
        f = open(filename[1:])
        outputdata = f.readlines()
        
        # Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())

        # Send the content of the requested file to the client
        for i in range(len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send('\r\n'.encode())

        connectionSocket.close()
    except IOError:
        # Send respone message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())

        # Close client socket
        connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
serverSocket.bind((HOST, PORT))
serverSocket.listen(100)

while True:
    # Establish the conneciton
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=work, args=(connectionSocket, addr)).start()
    

serverSocket.close()
sys.exit()