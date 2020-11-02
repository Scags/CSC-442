#!/usr/bin/env python3

from pynput.keyboard import Controller, Key
from time import sleep

def main():
	keyboard = Controller()

	pwd = input().strip().replace("[", "").replace("]", "")
	pwd = pwd.split(",")
	pwd = pwd[:len(pwd) // 2 + 1]
	for i in range(len(pwd)):
		pwd[i] = pwd[i].strip().replace("'", "")
	pwd = "".join(pwd)
	print(pwd)

	timings = input().strip().replace("'", "").replace("[", "").replace("]", "")
	timings = [float(a) for a in timings.split(",")]

	keypress = timings[:len(timings) // 2 + 1]
	keyinterval = timings[len(timings) // 2 + 1:]
	keyinterval.append(0.0)
	print(keypress)
	print(keyinterval)

	sleep(5.0)
	print("starting")
#	keyboard.press(Key.enter)
#	keyboard.release(Key.enter)
	sleep(5.0)

	i = 0
	for i, c in enumerate(pwd):
#		print(c)
		keyboard.press(c)
		sleep(keypress[i])
		keyboard.release(c)
		sleep(keyinterval[i])

	keyboard.press(Key.enter)
	keyboard.release(Key.enter)
	print("done")

if __name__ == "__main__":
	main()
