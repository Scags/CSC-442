#!/usr/bin/env python3

###################################
#
# TEAM PHOENIX
#
###################################

from time import mktime, strptime, time
from hashlib import md5

EPOCH_FORMAT = "%Y %m %d %H %M %S"
CURR_TIME = ""

def datetotimestamp(timestr:str) -> int:
	return int(mktime(strptime(timestr, EPOCH_FORMAT)))

def main():
	inputstr = input().strip()
	currtime = datetotimestamp(inputstr)
	inputtime = int(time()) if not CURR_TIME else datetotimestamp(CURR_TIME)

	hashtime = inputtime - currtime
	hashtime -= hashtime % 60	# Floor to minute

	hash1 = md5(str(hashtime).encode()).hexdigest()
	hash2 = md5(hash1.encode()).hexdigest()

	# Chars
	passwd = "".join([i for i in hash2 if i.isalpha()])[:2]
	# Digits
	passwd += "".join([i for i in reversed(hash2) if i.isdigit()])[:2]
	print(passwd)

if __name__ == "__main__":
	main()