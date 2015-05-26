#!/usr/bin/python

#################################################################
# Name: Client.Py
# Description: sends different UDP CMD through the network
#################################################################
import RPi.GPIO as GPIO
import time
import socket
import os
import sys, getopt
import logging
import logging.handlers


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def main(argv):
	CMD =''
	MESSAGE = ''
	UDP_IP = "127.0.0.1"
	UDP_PORT = 12121

	OldInputStatus=False
	CurrentInputStatus=False
	InputChanged=False
	
	### Logging Setup
	logging.basicConfig(level=logging.INFO)		#level=logging.DEBUG
	logger = logging.getLogger(__name__)
	
	# create a file handler
	handler = logging.FileHandler('Client.log')
	handler.setLevel(logging.INFO)
	
	#Create a logging format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	
	#add the handlers to the logger
	logger.addHandler(handler)
	
	
	### Command Line parameters reading
	logger.info('Getting Command Line Parameters')
	try:
		opts, args = getopt.getopt(argv,"hm:",["Ifile="])
	except getopt.GetoptError:
		print 'Client.py -m message'
		logger.error('Wrong Parameters entered',exc_info=True, *args)
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print 'Client.py -m <message>'
			sys.exit()
		elif opt in ("-m","--ifile"):
			CMD = arg
	
	if CMD =="" :
		MESSAGE = "Simpsons"
		logger.info('No CMD received through cmd line, using default =', MESSAGE)
	else :
		MESSAGE = CMD
		logger.info('CMD received through cmd line = %s', MESSAGE)

	while True:
		
		CurrentInputStatus = GPIO.input(18)
		
		if OldInputStatus <> CurrentInputStatus:
			OldInputStatus = CurrentInputStatus
			print "--------------------------\r\n Current Status:",CurrentInputStatus
			InputChanged = True
		
		if InputChanged == True:
			if CurrentInputStatus==False:
				MESSAGE = "Simpsons"
			InputChanged = False
	
		if MESSAGE<>"":
			print "--------------------------"
			print "UDP target IP:", UDP_IP
			print "UDP target port:", UDP_PORT
			print "message:", MESSAGE
			
			### Open UDP socket
			sock = socket.socket(socket.AF_INET, # Internet
								 socket.SOCK_DGRAM) # UDP
			sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

			sock.close
			
		MESSAGE=""
		
	
			
			
			
			
if __name__ == "__main__":
	main(sys.argv[1:])
	


