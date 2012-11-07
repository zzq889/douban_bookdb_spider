import time
lasttime = time.time()
flag = 0
while 1:
	print flag,
	flag += 1
	while flag == 10:
		if time.time() - lasttime >= 5:
			lasttime = time.time()
			flag = 0
			print
		else:
			time.sleep(1)
