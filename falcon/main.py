from core.note import Note
from core.data import Data
from core.page import Page

if __name__ == "__main__":
	note  = Note("./config.ini")
	notes = note.getsContent(1000)
	for key, note in notes.items():
		da = Data()
		da.addArticle(note)
		"""
		article = {
			"site_title":"耿鸿豪的博客",
			"site_desc":"努力工作，努力生活，记录美好生活！",
			"site_domain":"http://genghonghao.com",
			"blog_guid":note["guid"],
			"blog_subject":note["title"],
			"blog_author":"测试标题",
			"blog_content":note["content"],
			"blog_created":note["created"],
			"updated":note["updated"],
			"cate_guid":note["notebook_guid"],
			"cate_name":note["notebook_name"],
			"cate_url":"/archives/"+note["guid"]+"html",
			"copyright_info":"京ICP 3000011111",
			"previous_url":"/aaaaaaaa.html",
			"previous_subject":"xxxxxxxxxxxxxxxxxx",
			"next_url":"/aaaaaaaaafffffff.html",
			"next_subject":"dddddiiiiiii",
		}
		"""
		pa = Page("default", article)
		# 生成详情页
		pa.createDetail()
		# 生成首页
		# 生成分类列表页
		# 生成按日期列表页
