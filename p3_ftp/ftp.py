#!/usr/bin/env python3

##########################################
#
#	Group Phoenix
#
##########################################

from ftplib import FTP

# TODO?;
# I talked to Timo during this challenge, he mentioned about reading
# recursively through subdirectories
# I hope he was joking because that'd be a pain in the ass
# But let's be wary just in case that happens during the CyberStorm

# FTP server details
IP = "138.47.99.29"
PORT = 8008
USER = "valkyrie"
PASSWORD = "myfirstchallenge"
FOLDER = ".secretstorage/.folder2/.howaboutonemore"
USE_PASSIVE = True # set to False if the connection times out

# connect and login to the FTP server
ftp = FTP()
ftp.connect(IP, PORT)
ftp.login(USER, PASSWORD)
ftp.set_pasv(USE_PASSIVE)

# navigate to the specified directory and list files
ftp.cwd(FOLDER)
files = []

ftp.dir(files.append)

# exit the FTP server
ftp.quit()

# display the folder contents
outputstr_10 = ""
outputstr_7 = ""
for f in files:
	split = str(f).split(" ")
	perms = split[0]
	filename = split[-1]
	perm_bits = 0
	count = 0

	# This is stupidly complicated BUT, we are bit-ORing across our var if there isn't 
	# a "-" in our perms at this idx
	for i in range(len(perms)-1, -1, -1):
		perm_bits |= int(perms[i] != "-") << count
		count += 1

	# Yea, yea, yea, this is also silly but it works!
	# If we've got a bit beyond << 7 abort mission
	if not (perm_bits & 0xFFFFFF80):
		outputstr_7 += chr(perm_bits)
	outputstr_10 += f"{perm_bits:#012b}"[2:]

unpacked = [outputstr_10[i:i+7] for i in range(0, len(outputstr_10), 7)]

outputstr_10 = ""
for i in unpacked:
	outputstr_10 += chr(int(i, 2))

method = 0	# 0 -> 7bit
# Now figure out which is the better method
for c in outputstr_7:
	if ord(c) <= 0x1F:
		method = 1

print(outputstr_10 if method else outputstr_7)
