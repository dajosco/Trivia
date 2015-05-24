#!/usr/bin/python

import socket
import os
import sys, getopt

def main(argv):
	CMD = ''
	try:
		opts, args = getopt.getopt(argv,"hm:",["Ifile="])
	except getopt.GetoptError:
		print 'Client.py -m message'
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print 'Client.py -m <message>'
			sys.exit()
		elif opt in ("-m","--ifile"):
			CMD = arg

	UDP_IP = "127.0.0.1"
	UDP_PORT = 12121
	if CMD =="" :
		MESSAGE = "Simpsons"
	else :
		MESSAGE = CMD
	

	print "UDP target IP:", UDP_IP
	print "UDP target port:", UDP_PORT
	print "message:", MESSAGE

	sock = socket.socket(socket.AF_INET, # Internet
						 socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

	sock.close
			
			
			
			
if __name__ == "__main__":
	main(sys.argv[1:])
	


