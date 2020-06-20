#-*- coding:utf-8 -*-
from utils.myfile import createJsonFile
from utils.myfile import readJsonFile

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
		json_data = sorted(json_data, key=lambda keys:keys['created'], reverse=True)
		return json_data

	# 获取当前记录的上条记录和下一条记录
	def fetchPrevAndNext(self, guid):
		json_data = self.fetchItems()
		cur_index = None
		for index, row in enumerate(json_data):
			if guid == row["guid"]:
				cur_idx = index
				break
		if None == cur_idx: return None, None
		next_idx = cur_idx - 1
		if next_idx >= 0:
			next_row = json_data[next_idx]
		else:
			next_row = None

		prev_idx = cur_idx + 1
		if (len(json_data) - 1) < prev_idx:
			prev_row = None
		else:
			prev_row = json_data[prev_idx]

		return prev_row, next_row


	# 获取最新一篇文章
	def fetchLatestItem(self):
		json_data = self.fetchItems()
		return json_data[0]

	# 获取最近10篇文章
	def fetchRecentItems(self, number):
		json_data = self.fetchItems()
		return json_data[0:number]

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
			if categuid == row["notebook_guid"]: ret_data.append(row)
		return ret_data

	# 获取所有分类信息
	def fetchCategory(self):
		json_data = self.fetchItems()
		ret_data  = {}
		for _, row in enumerate(json_data):
			key = row["notebook_guid"]
			if key in ret_data:
				ret_data[key]["number"] = 1 + ret_data[key]["number"]
			else:
				ret_data[key] = {"number":1, "name":row["notebook_name"], "notebook_guid":key} 

		# 将数据转化为列表
		ret_list = []
		for row in ret_data.items():
			ret_list.append(row[1])
		return ret_list
