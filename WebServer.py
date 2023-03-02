# import socket module
from socket import *
import sys

HOST = '0.0.0.0'
PORT = 8082

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)

while True:
    # Establish the conneciton
    print('Ready to server...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(2048)
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
    except IOError as e:
        # Send respone message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode())

        # Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()