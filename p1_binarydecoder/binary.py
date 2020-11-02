#!/usr/bin/env python3

# Flick on to account for backspaces in the input
LOOK_AT_TRASH = 0

def main():
	s = input()

	val = 7 if len(s) % 7 == 0 else 8
	unpacked = [s[i:i+val] for i in range(0, len(s), val)]
	outputstr = "".join([chr(int(i, 2)) for i in unpacked])
	print(outputstr)
	if LOOK_AT_TRASH:
		print(outputstr.encode())

if __name__ == "__main__":
	main()
