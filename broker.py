from time import sleep
import sys
import signal
from socket import *
from threading import Thread

#Receive packets from source with TCP and send them with UDP to destination. First receive message if its empty continue, if not extract sequence number and calculate modulo 3 and forward with different ips.
def receiver1():
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',25698))
	serverSocket.listen(1)
	global i
	while True:
		connectionSocket, addr = serverSocket.accept()
		message = connectionSocket.recv(1024)
		if message == "":
			connectionSocket.close()
			continue
		index=message.rfind('*')
		mess=int(message[index+1:])
		if mess%3==0:
			clientSocket = socket(AF_INET, SOCK_DGRAM)
			clientSocket.sendto(message,('10.10.3.2',25699))
			clientSocket.close()
		if mess%3==1:
			clientSocket = socket(AF_INET, SOCK_DGRAM)
			clientSocket.sendto(message,('10.10.5.2',25799))
			clientSocket.close()
		if mess%3==2:
                        clientSocket = socket(AF_INET, SOCK_DGRAM)
                        clientSocket.sendto(message,('10.10.5.2',25899))
                        clientSocket.close()
		connectionSocket.close()



def receiver2():
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',25798))
	serverSocket.listen(1)
	global i
	while True:
		connectionSocket, addr = serverSocket.accept()
		message = connectionSocket.recv(1024)
		if message == "":
			connectionSocket.close()
                        continue
		index=message.rfind('*')
		mess=int(message[index+1:])
                if mess%3==0:
                        clientSocket = socket(AF_INET, SOCK_DGRAM)
                        clientSocket.sendto(message,('10.10.3.2',25699))
                        clientSocket.close()
                if mess%3==1:
                        clientSocket = socket(AF_INET, SOCK_DGRAM)
                        clientSocket.sendto(message,('10.10.5.2',25799))
                        clientSocket.close()
                if mess%3==2:
                        clientSocket = socket(AF_INET, SOCK_DGRAM)
                        clientSocket.sendto(message,('10.10.5.2',25899))
                        clientSocket.close()
		connectionSocket.close()

def receiver3():
	serverSocket = socket(AF_INET,SOCK_STREAM)
	serverSocket.bind(('',25898))
	serverSocket.listen(1)
	global i
	while True:
		connectionSocket, addr = serverSocket.accept()
		message = connectionSocket.recv(1024)
		if message == "":
			connectionSocket.close()
                        continue
		index=message.rfind('*')
		mess=int(message[index+1:])
                if mess%3==0:
                        clientSocket = socket(AF_INET, SOCK_DGRAM)
                        clientSocket.sendto(message,('10.10.3.2',25699))
                        clientSocket.close()
                if mess%3==1:
                        clientSocket = socket(AF_INET, SOCK_DGRAM)
                        clientSocket.sendto(message,('10.10.5.2',25799))
                        clientSocket.close()
                if mess%3==2:
                        clientSocket = socket(AF_INET, SOCK_DGRAM)
                        clientSocket.sendto(message,('10.10.5.2',25899))
                        clientSocket.close()
		connectionSocket.close()

# Receive ack from destination with UDP and forward them directly to source by TCP
def ackReceiver():
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('',17000 ))
	while True:
		message, clientAddress = serverSocket.recvfrom(2048)
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect(('10.10.1.1',16000))
		clientSocket.send(message)
		clientSocket.close()

def ackReceiver1():
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('',17001 ))
	while True:
		message, clientAddress = serverSocket.recvfrom(2048)
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect(('10.10.1.1',16001))
		clientSocket.send(message)
		clientSocket.close()
def ackReceiver2():
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('',17002 ))
        while True:
                message, clientAddress = serverSocket.recvfrom(2048)
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect(('10.10.1.1',16002))
                clientSocket.send(message)
                clientSocket.close()


# Codes for threading
receiver1 = Thread(target = receiver1)
receiver2 = Thread(target = receiver2)
receiver3 = Thread(target = receiver3)
ackReceiver = Thread(target = ackReceiver)
ackReceiver1 = Thread(target = ackReceiver1)
ackReceiver2 = Thread(target = ackReceiver2)


receiver1.start()
receiver2.start()
receiver3.start()
ackReceiver.start()
ackReceiver1.start()
ackReceiver2.start()





