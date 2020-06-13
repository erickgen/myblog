#-*- coding:utf-8 -*-
from libs.template import Template
from utils.myfile import createFile
from utils.myfile import readFile

class Page:
	def __init__(self, theme_name, article):
		self.theme_name = theme_name
		self.article = article

	# 生成文章详情页
	def createDetail(self):
		tpl_file = './themes/' + self.theme_name + '/detail.html'
		if False == tpl_file: return False
		tpl_html = readFile(tpl_file)

		template  = Template(tpl_html)
		page_html = template.assign(self.article)

		page_file = "./html/archives/"+self.article["blog_guid"]+".html"
		createFile(page_file, page_html)

		return True

	def createHome(self):
		pass
	
	def createCate(self):
		pass

	def createDate(self):
		pass
