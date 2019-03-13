from time import sleep
import time
import sys
import signal
from socket import *
from threading import Thread 


RecInd = [0]*6250 #Store which data are received and stored into DataReceived
DataReceived = [0]*6250 #Store received data to write to file
counter=0

# To halt scripts
def signal_handler(signal, frame):
	sys.exit(0)

def chksum(data):
	res=0
	for x in data:
		res+=ord(x)
	return ~res

def sum(data):
	res=0
	for x in data:
		res+=ord(x)
	return res

# Receive packets if not empty divides its into three pieces checksum, message and sequence number. Then store it into Data array according to sequence number. Then forward sequence number as ack to broker to send source.
def Receiver():
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('',25699 ))
	global counter
	while True:
		message, clientAddress = serverSocket.recvfrom(2048)
		if message=="":
			continue
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		index1 = message.find('*')
		index2= message.rfind('*')
		fmess=message[:index1]
		smess=int(message[index1+1:index2])
		tmess=int(message[index2+1:])
		if (sum(fmess)+smess)== -1 and RecInd[tmess]==0:
			DataReceived[tmess]=fmess
			RecInd[tmess]=1
			counter+=1
		if (sum(fmess)+smess)== -1 and RecInd[tmess]==1:
			clientSocket.sendto(str(tmess),('10.10.1.2', 17000))
		clientSocket.close()

def Receiver1():
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('',25799 ))
	global counter
	while True:
		message, clientAddress = serverSocket.recvfrom(2048)
		if message=="":
                        continue
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		index1 = message.find('*')
		index2= message.rfind('*')
		fmess=message[:index1]
		smess=int(message[index1+1:index2])
		tmess=int(message[index2+1:])
		if (sum(fmess)+smess)== -1 and RecInd[tmess]==0:
			DataReceived[tmess]=fmess
			RecInd[tmess]=1
			counter+=1
		if (sum(fmess)+smess)== -1 and RecInd[tmess]==1:
			clientSocket.sendto(str(tmess),('10.10.2.1', 17001))
		clientSocket.close()

def Receiver2():
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('',25899 ))
        global counter
        while True:
                message, clientAddress = serverSocket.recvfrom(2048)
                if message=="":
                        continue
                clientSocket = socket(AF_INET, SOCK_DGRAM)
                index1 = message.find('*')
                index2= message.rfind('*')
                fmess=message[:index1]
                smess=int(message[index1+1:index2])
                tmess=int(message[index2+1:])
                if (sum(fmess)+smess)== -1 and RecInd[tmess]==0:
                        DataReceived[tmess]=fmess
                        RecInd[tmess]=1
                        counter+=1
                if (sum(fmess)+smess)== -1 and RecInd[tmess]==1:
                        clientSocket.sendto(str(tmess),('10.10.2.1', 17002))
                clientSocket.close()

# For threading
receiver = Thread(target = Receiver)
receiver1 = Thread(target = Receiver1)
receiver2 = Thread(target = Receiver2)


receiver.daemon= True
receiver1.daemon= True
receiver2.daemon=True

receiver.start()
receiver1.start()
receiver2.start()

#If all datas are received then write them into file and halt.
while True:
	if counter==6250:
		start_time = time.time()
		print "successful!",str(start_time)
		with open('output.txt', 'w') as f:
    			for item in DataReceived:
        			f.write("%s" % item)
		sleep(3)
		signal.signal(signal.SIGINT, signal_handler)
		break

		
