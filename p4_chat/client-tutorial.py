#!/usr/bin/env python3

import socket
from sys import stdout
from time import time
from binascii import unhexlify

# NOTE; this has been edited to account for the challenge

# enables debugging output
DEBUG = False
TIME_DELTA = 0.3

# set the server's IP address and port
ip = "138.47.99.5"
port = 54321

# create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	# connect to the server
	s.connect((ip, port))

	# receive data until EOF
	data = s.recv(4096)
	encoded = ""
	fullmsg = ""
	while (data.rstrip(b"\n") != b"EOF"):
		# output the data
		stdout.write(str(data)[1:].strip("'"))
		if r"\n" in str(data)[1:].strip("'"):
			fullmsg += encoded
			encoded = ""
#			break

		stdout.flush()
		# start the "timer", get more data, and end the "timer"
		t0 = time()
		data = s.recv(4096)
		t1 = time()
		# calculate the time delta (and output if debugging)
		delta = round(t1 - t0, 3)
		encoded += ("1" if delta > TIME_DELTA else "0")
#		print(encoded)
		if (DEBUG):
			stdout.write(" {}\n".format(delta))
			stdout.flush()

	covert = ""
	for i in range(0, len(fullmsg), 8):
		b = fullmsg[i:i+8]
		n = int("0b{}".format(b), 2)
		try:
			h = int("{0:x}".format(n), 16)
			if h > 0x1f and h <= 0x7D:
				covert += chr(h)
			else:
				covert += "?"
		except:
			covert += "?"

		if covert.endswith("EOF"):
			covert = covert[:-3]
			break

	print()
	print(covert)

except Exception as e:
	print(e)

# close the connection to the server
s.close()
