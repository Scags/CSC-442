#!/usr/bin/env python3

###################################
#
# TEAM PHOENIX
#
###################################

from sys import stdin, stdout

KEY = "key"

def main():
	inpt = ""
	# Python tries to force everything as Unicode
	# This wouldn't be a problem with py 2 <= (That uses utf-8)
	# But we don't have that luxury so we fix it ourselves with .buffer! \o/
#	stdin.reconfigure(encoding = "utf-8")
	while not inpt:
		inpt = stdin.buffer.read().strip()

#	print(inpt)
	l1 = bytearray(inpt)

#	print(l1)

	l2 = []
	with open(KEY, "rb") as f:
		while b := f.read(1):	# Walrus ops are fun (Python 3.8+)
			l2.append(ord(b))

	l2 = bytearray(l2)
#	print(l2)

	# to_bytes supersedes conventional encoding. Has to do with endianness maybe?
	final = [(a ^ b).to_bytes(1, byteorder = "big") for (a, b) in zip(l1, l2)]
#	print(final)

	stdout.buffer.write(b"".join(final))

if __name__ == "__main__":
	main()