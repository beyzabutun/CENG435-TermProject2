import time
from time import sleep
import sys
import signal
from socket import *
from threading import Thread


wnd_size=127 #This is a indicator that indicates the end of the window
cwndLocation=0 #This is a indicator that indicates the beginning of the window
i=0 #This is a variable for sending packets

f=open('input.txt','r')
inp=f.read()

messageS=[0]*6250 #This is an array that store the pakcets which derived from file
count=0 #To count packets that successfuly sent
count1=0 #To divide file into packets
count2=800 #To divide file into packets

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',16000))
serverSocket.listen(1)
serverSocket2 = socket(AF_INET,SOCK_STREAM)
serverSocket2.bind(('',16001))
serverSocket2.listen(1)
serverSocket3 = socket(AF_INET,SOCK_STREAM)
serverSocket3.bind(('',16002))
serverSocket3.listen(1)

#Divide file into packets then store in messageS array
for x in range (0,6250):
	messageS[x]=inp[count1:count2]
	count1=count2
	count2=count2+800

DataSended= [0]*6251 #For selective repeat, this shows the successfuly sent packets

start_time = time.time()
# print start_time

#method to halt scripts
def signal_handler(signal, frame):
	sys.exit(0)

def chksum(data):
	res=0
	for x in data:
		res+=ord(x)
	return ~res

# To send packets, there three of them
def sender1():
	global i
	while True:
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect(('10.10.1.2',25698))
		if i<6250 and DataSended[i]==0 and (i-cwndLocation)<128: # send if not exceed window, array and not sended before
			mess=messageS[i]+'*'+str(chksum(messageS[i]))+'*'+str(i)
			clientSocket.send(mess)
		if (i-cwndLocation)<128:
			i+=1
		clientSocket.close()

def sender2():
	global i
	while True:

		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect(('10.10.2.1',25798))
		if i<6250 and DataSended[i]==0 and (i-cwndLocation)<128:
			mess=messageS[i]+'*'+str(chksum(messageS[i]))+'*'+str(i)
			clientSocket.send(mess)
		if (i-cwndLocation)<128:
			i+=1
		clientSocket.close()

def sender3():
	global i
	while True:
		clientSocket = socket(AF_INET, SOCK_STREAM)
		clientSocket.connect(('10.10.4.1',25898))
		if i<6250 and DataSended[i]==0 and (i-cwndLocation)<128:
			mess=messageS[i]+'*'+str(chksum(messageS[i]))+'*'+str(i)
			clientSocket.send(mess)
		if (i-cwndLocation)<128:
			i+=1
		clientSocket.close()

# For selective repeat and go back n
def timer():
	global i
	while True:
		sleep(1.5)
		i=cwndLocation
		print i, cwndLocation
		wnd_size=i+127

#Function that count successfuly sent packet via receiving ACKs
def ackReceiver():
	global i
	global cwndLocation
	global wnd_size
	global count
	while True:
		connectionSocket, addr = serverSocket.accept()
		message = connectionSocket.recv(1024)
		if message=="": #if message is empty then continue
			connectionSocket.close()
			continue
		li=DataSended.index(0) #find first not successfuly sent packet number
		index=int(message)
		DataSended[index]=1
		ii=DataSended.index(0) #find first not successfuly sent packet number after received one more ACK
		count+=1
		if index== li: #if last received ack goes into beginning of actual window then update cwnd locaton
			cwndLocation=ii
		connectionSocket.close()

def ackReceiver2():
        global i
        global cwndLocation
        global wnd_size
        global count
        while True:
                connectionSocket, addr = serverSocket2.accept()
                message = connectionSocket.recv(1024)
                if message=="":
                        connectionSocket.close()
                        continue
                li=DataSended.index(0)
                index=int(message)
                DataSended[index]=1
                ii=DataSended.index(0)
                count+=1
                if index== li:
                        cwndLocation=ii
                connectionSocket.close()

def ackReceiver3():
        global i
        global cwndLocation
        global wnd_size
        global count
        while True:
                connectionSocket, addr = serverSocket3.accept()
                message = connectionSocket.recv(1024)
                if message=="":
                        connectionSocket.close()
                        continue
                li=DataSended.index(0)
                index=int(message)
                DataSended[index]=1
                ii=DataSended.index(0)
                count+=1
                if index== li:
                        cwndLocation=ii
                connectionSocket.close()


sender1 = Thread(target = sender1)
sender2 = Thread(target = sender2)
sender3 = Thread(target = sender3)
timer1 = Thread(target = timer)
ackReceiver1 = Thread(target = ackReceiver)
ackReceiver2 = Thread(target = ackReceiver2)
ackReceiver3 = Thread(target = ackReceiver3)



sender1.daemon= True
sender2.daemon= True
sender3.daemon= True
timer1.daemon = True

ackReceiver1.daemon = True
ackReceiver2.daemon  =True
ackReceiver3.daemon  =True
sender1.start()
sender2.start()
sender3.start()
timer1.start()
ackReceiver1.start()
ackReceiver2.start()
ackReceiver3.start()

# If all packets sent successfuly then halt
while True:
	if cwndLocation == 6250:
		print "You had received!"
		signal.signal(signal.SIGINT, signal_handler)
		break









