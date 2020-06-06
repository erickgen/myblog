import os

# 取得文章列表
def getArticleList(filename):
	if not os.path.isfile(filename): return None

	fd = open(filename, "r")
	data_str = fd.read()
	data_arr = data_str.split("\n")
	data_arr.reverse()
	for key, row in data_arr:
		data_arr[key] = row.split("|")

	return data_arr


# 更新文章索引
def updateArticleIndex(filename, flag, title, created):
	row_data = flag + "|" + title + "|" + created + "\n"
	if not os.path.isfile(filename):
		fd = open(filename, mode="w+", encoding="utf-8")
		fd.write(row_data)
		fd.close()
		return 
	fd = open(filename, mode="a+", encoding="utf-8")
	fd.write(row_data)
	fd.close()
	return 

# 取得最后更新文章标识
def getLatestArticleFlag(filename):
	if not os.path.isfile(filename): return None

	fd = open(filename, "r")
	return fd.read()

# 更新最后更新文章标识
def updateLatestArticleFlag(filename, flag):
	fd = open(filename, mode="w+", encoding="utf-8")
	fd.write(flag)
	fd.close()
