import sys

def getRootPath():
	return sys.path[0][0:-6]

def getHtmlPath():
	return getRootPath()+"/html"

def getDataPath():
	return getRootPath()+"/data"
"""
if __name__=="__main__":
	r = getDataPath()
	print(r)
"""
