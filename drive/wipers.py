import os
import time

delay = 0.5

while True:
	time.sleep(delay)
	os.system("echo 0=0% > /dev/servoblaster")
	time.sleep(delay)
	os.system("echo 0=100% > /dev/servoblaster")
