#-*- coding:utf-8 -*-

# 生成文件
def createFile(filename, content):
	fp = open(filename, 'w')
	fp.write(content)
	fp.close()

#以json格式写入文件
def createJsonFile(fileName, content):
    fp = open(fileName, "w")
	fp.write(json.dumps(content, indent=4, ensure_ascii=False))
	fp.close()

# 读取Json数据
def readJsonFile(fileName):
    if False == os.path.exists(fileName):
        return False
    with open(fileName,'r') as load_f: load_dict = json.load(load_f)
    return load_dict
