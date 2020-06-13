#-*- coding:utf-8 -*-

import os
import json

# 生成文件
def createFile(filename, content):
	fp = open(filename, 'w')
	fp.write(content)
	fp.close()

# 读取文件
def readFile(filename):
	if False == os.path.exists(filename): return False
	fo   = open(filename, "r+")
	content = fo.read()
	fo.close()
	return content

#以json格式写入文件
def createJsonFile(filename, content):
	fp = open(filename, "w")
	fp.write(json.dumps(content, indent=4, ensure_ascii=False))
	fp.close()

# 读取Json数据
def readJsonFile(filename):
    if False == os.path.exists(filename): return False
    with open(filename,'r') as load_f: load_dict = json.load(load_f)
    return load_dict
