#!/usr/bin/env python3

from sys import argv

# Assume Encrypt if no argument is provided
# Python enums are silly so this works
Method_Encrypt = 0
Method_Decrypt = 1
def getmethod() -> int:
	method = Method_Encrypt

	if len(argv) <= 1:
		return method

	# Lazy, but why would someone provide any other type of argument?
	return {"-e": Method_Encrypt, "-d": Method_Decrypt}.get(argv[1], Method_Encrypt)

def getkey(method:int) -> str:
	s = "encrypt" if method is Method_Encrypt else "decrypt"
	k = argv[2] if len(argv) > 2 else str(input(f"Please provide a key to {s}: "))

	while not len(k):
		k = str(input(f"Invalid key provided\nPlease provide a key to {s}: "))
	return k

def vigenere(inpt:str, key:str, method:int) -> None:
	key = "".join([c for c in key if c.isalpha()])
	keylen = len(key)
	s = ""
	keycount = 0

	for c in inpt:
		if not c.isalpha():
			s += c
			continue

		shouldcapitalize = c.isupper()
		lower = c.lower()

		print(key[keycount % keylen], c)

		# 0x61 is the lowest lowercase ASCII value or 'a'
		# Since everything is forced to lowercase, we subtract by that value, then we can 
		# successfully mod by 26 without getting a garbage value
		e = ord(lower) - 0x61
		k = ord(key[keycount % keylen]) - 0x61
		if method is Method_Decrypt:
			k = -k + 26

		val = (e + k) % 26
		s += chr(val + (0x41 if shouldcapitalize else 0x61))
		keycount += 1

	print(s)

def main() -> None:
	method = getmethod()
	key = getkey(method).lower()	# No caps allowed

	while 1:
		inpt = str(input())

		if not len(inpt):
			continue

		vigenere(inpt, key, method)

if __name__ == "__main__":
	main()