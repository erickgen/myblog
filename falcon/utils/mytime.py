import time

def formatDate(timenum):
	timestamp = float(timenum / 1000)
	timearray = time.localtime(timestamp)
	return time.strftime("%Y-%m-%d", timearray)
