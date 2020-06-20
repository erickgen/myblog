#-*- coding:utf-8 -*-

import os
import json
import shutil

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

# 复制目录
def copyDir(oridir, targetdir):
	shutil.copytree(oridir, targetdir)

# 删除目录
def delDir(mypath):
	if os.path.exists(mypath): shutil.rmtree(mypath)
