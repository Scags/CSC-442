#!/usr/bin/env python3

###################################
#
# TEAM PHOENIX
#
###################################

import argparse
from enum import IntEnum
from os import path
from sys import stdout

class Mode(IntEnum):
	Store = 0
	Retrieve = 1

class Method(IntEnum):
	Bit = 0
	Byte = 1

parser = argparse.ArgumentParser(description = "Perform the Steg algorithm on a file")
parser.add_argument("-s", action = "store_const", 				help = "Store data", 	const = Mode.Store, 	dest = "MODE")
parser.add_argument("-r", action = "store_const", 				help = "Retrieve data", const = Mode.Retrieve, 	dest = "MODE")
parser.add_argument("-b", action = "store_const", 				help = "Bit mode", 		const = Method.Bit, 	dest = "METHOD")
parser.add_argument("-B", action = "store_const", 				help = "Byte mode", 	const = Method.Byte, 	dest = "METHOD")
parser.add_argument("-o", nargs = "?", default = 0, type = int, help = "Set offset to <val> (default 0)",  		dest = "OFFSET")
parser.add_argument("-i", nargs = "?", default = 1, type = int, help = "Set interval to <val> (default 1)", 	dest = "INTERVAL")
parser.add_argument("-w", nargs = "?", required = 1,type = str, help = "Set wrapper to file <val>",				dest = "WRAPPER")
# NOTE: -h is used by argparse as the help command. This means -h(idden) is replaced with -H!
parser.add_argument("-H", nargs = "?",				type = str, help = "Set hidden to file <val>",				dest = "HIDDEN")
args = parser.parse_args()

# Arguments
METHOD = args.METHOD
MODE = args.MODE
OFFSET = args.OFFSET
INTERVAL = args.INTERVAL
WRAPPER = args.WRAPPER
HIDDEN = args.HIDDEN

# Other data
SENTINEL = bytearray([0x0, 0xFF, 0x0, 0x0, 0xFF, 0x0])

def store(wrapper, hidden):
	global OFFSET
	if METHOD == Method.Byte:
		# Byte method
		for b in hidden:
			wrapper[OFFSET] = b
			OFFSET += INTERVAL
		for b in SENTINEL:
			wrapper[OFFSET] = b
			OFFSET += INTERVAL
	else:
		# Bit method
		hidden += SENTINEL
		for i in range(len(hidden)):
			currhidden = hidden[i] & 0xFF

			for _ in range(8):
				currwrapper = wrapper[OFFSET]
				currwrapper &= ~1
				currwrapper |= currhidden >> 7
				currhidden <<= 1
				currhidden &= 0xFF	# Keep it <= 255. This probably isn't needed?

				wrapper[OFFSET] = currwrapper
				OFFSET += INTERVAL

	# BRUH https://bugs.python.org/issue24892
	stdout.buffer.write(b"".join(wrapper[i:i+1] for i in range(len(wrapper))))

def retrieve(wrapper):
	global OFFSET
	data = b""
	found = False

	if METHOD == Method.Byte:
		while not found and len(wrapper) > OFFSET:
			data += wrapper[OFFSET].to_bytes(1, byteorder = "big")
			OFFSET += INTERVAL

			if len(data) >= len(SENTINEL):
				for i in range(len(SENTINEL)):
					if data[i-len(SENTINEL)] != SENTINEL[i]:
						break

					if i == len(SENTINEL)-1:
						data = data[:-len(SENTINEL)]
						found = True
	else:
		while not found and len(wrapper) > OFFSET + 7:
			byte = 0
			for i in range(8):
				bit = wrapper[OFFSET] & 1
				byte |= bit
				if i < 7:
					byte <<= 1

				OFFSET += INTERVAL

			data += byte.to_bytes(1, byteorder = "big")
			if len(data) >= len(SENTINEL):
				for i in range(len(SENTINEL)):
					if data[i-len(SENTINEL)] != SENTINEL[i]:
						break

					if i == len(SENTINEL)-1:
						data = data[:-len(SENTINEL)]
						found = True

	stdout.buffer.write(data)

def main():
	with open(WRAPPER, "rb") as f:
		if not f:
			print(f"Invalid file wrapper file \"{WRAPPER}\" specified")
			return
		wrapper = bytearray(f.read()[:-1])		# Strip newline

	if MODE == Mode.Store:
		with open(HIDDEN, "rb") as f:
			if not f:
				print(f"Invalid file hidden file \"{HIDDEN}\" specified")
				return
			hidden = bytearray(f.read()[:-1])		# Strip newline
		store(wrapper, hidden)
	else:
		retrieve(wrapper)

if __name__ == "__main__":
	main()