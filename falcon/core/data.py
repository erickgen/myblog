#-*- coding:utf-8 -*-
from utils.myfile import createJsonFile
from utils.myfile import readJsonFile

'''
json_item ={
	"subject":"测试标题",
	"guid":"abcdefgamadd",
	"created":"2020-05-29",
	"cate_guid":"xxxxx",
	"cate_name":"xxxxx",
}
'''

class Data:
	def __init__(self):
		self.filename = "./data/articles.json"

	# 添加新文章
	def addArticle(self, item):
		ret = readJsonFile(self.filename)
		if False == ret:
			json_data = [item]
		else:
			content = readJsonFile(self.filename)

			is_new = True
			for index, row in enumerate(content):
				if row["guid"] == item["guid"]: is_new = False

			if True == is_new: content.insert(0, item)

			json_data = content
		createJsonFile(self.filename, json_data)
		return True

	# 读取数据内容
	def fetchItems(self):
		json_data = readJsonFile(self.filename)
		return json_data

	# 获取最新一篇文章
	def fetchLatestItem(self):
		json_data = self.fetchItems()
		return json_data[0]

	# 获取最近10篇文章
	def fetchRecentItems(self):
		json_data = self.fetchItems()
		return json_data[0:10]

	# 获取年度文章
	def fetchArticlesByYear(self):
		json_data = self.fetchItems()
		ret_data  = {}
		for _, row in enumerate(json_data):
			year = row["created"][0:4]
			ret_data[year].append(row)
		return ret_data

	# 获取年度列表
	def fetchYears(self):
		json_data = self.fetchItems()
		ret_data  = {}
		for _, row in enumerate(json_data):
			key = row["created"][0:4]
			if False == ret_data.has_key(key):
				ret_data[key] = {"number":1, "name":key} 
			else:
				ret_data[key]["number"] += ret_data[key]["number"]

		return ret_data

	# 获取分类文章
	def fetchArticlesByCateGuid(self, categuid):
		json_data = self.fetchItems()
		ret_data  = []
		for _, row in enumerate(json_data):
			if categuid == row["cate_guid"]: ret_data.append(row)
		return ret_data

	# 获取所有分类信息
	def fetchCates(self):
		json_data = self.fetchItems()
		ret_data  = {}
		for _, row in enumerate(json_data):
			key = row["cate_guid"]
			if False == ret_data.has_key(key):
				ret_data[key] = {"number":1, "name":row["cate_name"]} 
			else:
				ret_data[key]["number"] += ret_data[key]["number"]

		return ret_data
