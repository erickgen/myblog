#-*- coding:utf-8 -*-
from libs.template import Template
from utils.myfile import createFile
from utils.myfile import readFile
from utils.myfile import delDir
from utils.myfile import copyDir

class Page:
	def __init__(self, theme_name):
		self.theme_path = './themes/' + theme_name
		self.html_path  = './html'
		self.root_path  = ''

	# 更新静态资源
	def updateAssets(self):
		target_path = self.html_path + "/assets"
		delDir(target_path)
		copyDir(self.theme_path+"/assets", target_path)


	# 取得html文件路径
	def fetchPageUrl(self, pagekey, pagename):
		if "detail" == pagekey:
			return self.root_path + '/archives/' + pagename + '.html'
		elif "index" == pagekey:
			return self.root_path + '/index.html'
		elif "category" == pagekey:
			return self.root_path + '/category/' + pagename + '.html'
		elif "date" == pagekey:
			return self.root_path + '/date/' + pagename + '.html'
		return None

	
	# 模板和html的对应关系
	def templateHtmlRelation(self, pagekey, pagename):
		ret = {}
		if "detail" == pagekey:
			ret = {
				"tpl_file":self.theme_path + '/detail.html',
				"page_file":self.html_path + '/archives/' + pagename + '.html'
			}
		elif "index" == pagekey:
			ret = {
				"tpl_file":self.theme_path + '/index.html',
				"page_file":self.html_path + '/' + pagename + '.html'
			}
		elif "category" == pagekey:
			ret = {
				"tpl_file":self.theme_path + '/category.html',
				"page_file":self.html_path + '/category/' + pagename + '.html'
			}
		elif "archives" == pagekey:
			ret = {
				"tpl_file":self.theme_path + '/archives.html',
				"page_file":self.html_path + '/' + pagename + '.html'
			}
		return ret

	# 生成页面
	def createPage(self, pagekey, pagename, assigndata):
		thr = self.templateHtmlRelation(pagekey, pagename)
		tpl_content = readFile(thr['tpl_file'])

		template  = Template(tpl_content)
		page_content = template.assign(assigndata)

		createFile(thr['page_file'], page_content)

		return True


	# 生成文章详情页
	def createDetail(self, guid, data):
		return self.createPage("detail", guid, data)

	def createIndex(self, data):
		return self.createPage("index", "index", data)
	
	def createCategory(self, notebookguid, data):
		return self.createPage("category", notebookguid, data)

	def createArchives(self, data):
		return self.createPage("archives", "archives", data)
