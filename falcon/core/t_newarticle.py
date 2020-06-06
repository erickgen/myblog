#-*- coding:utf-8 -*-
import json
import os

'''
测试存储最新文章列表文件
'''
fileName = "./data/LatestArticle.json"
#要写入文件的json串（dict格式）
inData ={
	"subject":"测试标题",
	"guid":"abcdefgamadd",
	"created":"2020-05-29",
}
#以json格式写入文件
def createFile(fileName, inData):
	with open(fileName, "w") as fp: fp.write(json.dumps(inData, indent=4, ensure_ascii=False))

# 读取Json数据
def readFile(fileName):
	if False == os.path.exists(fileName):
		return False
	with open(fileName,'r') as load_f: load_dict=json.load(load_f)
	return load_dict

def updateLatestArticle(inData):
	fileName = "./data/LatestArticle.json"
	ret = readFile(fileName)
	if False == ret:
		json_data = [inData]
	else:
		content = readFile(fileName)
		content.insert(0, inData)

		repeat = False
		for index, row in enumerate(content):
			if 0 == index: continue
			print(row["guid"])
			print(inData["guid"])
			if row["guid"] == inData["guid"]:
				del content[index]
				repeat = True
				break;

		if False == repeat and len(content) > 20:
			content.pop()

		json_data = content
	createFile(fileName, json_data)
updateLatestArticle(inData)
s = readFile(fileName)
print(s)
"""
print(type(load_dict),load_dict)
createFile(fileName, inData)
s = readFile(fileName)
"""
# 分类文章数据
# 更新更多文章列表页
# 生成文章分类页
# 生产首页
# 更新统计数据
