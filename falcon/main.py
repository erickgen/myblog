import configparser

from core.note import Note
from core.data import Data
from core.page import Page

if __name__ == "__main__":
	conf = configparser.ConfigParser(allow_no_value=True)
	conf.read("./config.ini")

	site_title     = conf.get("site", "title")
	site_desc      = conf.get("site", "desc")
	site_domain    = conf.get("site", "domain")
	site_copyright = conf.get("site", "copyright")

	note  = Note("./config.ini")
	notes = note.getsContent(1000)
	pa = Page("default")
	da = Data()

    # 文章分类
	cates = da.fetchCategory()

    # 更新资源文件
	pa.updateAssets()

	# 写入数据
	for _, note in enumerate(notes): da.addArticle(note)

	# 生成文章
	for _, note in enumerate(notes):
		prev_data, next_data = da.fetchPrevAndNext(note["guid"])
		if None == prev_data:
			prev_url = "#"
			prev_title = "#"
		else:
			prev_url = pa.fetchPageUrl("detail", prev_data["guid"])
			prev_title = prev_data["title"]

		if None == next_data:
			next_url = "#"
			next_title = "#"
		else:
			next_url = pa.fetchPageUrl("detail", next_data["guid"])
			next_title = next_data["title"]

		article = {
			"site_title":site_title,
			"site_desc":site_desc,
			"site_domain":site_domain,
			"site_copyright":site_copyright,
			"guid":note["guid"],
			"title":note["title"],
			"author":"测试标题",
			"content":note["content"],
			"created":note["created"],
			"updated":note["updated"],
			"notebook_guid":note["notebook_guid"],
			"notebook_name":note["notebook_name"],
			"notebook_url":pa.fetchPageUrl("category", note["notebook_guid"]),
			"prev_url":prev_url,
			"prev_title":prev_title,
			"next_url":next_url,
			"next_title":next_title,
		}

		# 生成详情页
		pa.createDetail(article["guid"], article)

	# 生成首页
	articles = da.fetchRecentItems(8)
	for index, row in enumerate(articles):
		if 0 == index: articles[index]['introduction'] = row['content'][0:56]
		articles[index]["url"] = pa.fetchPageUrl("detail", row["guid"])
		del(articles[index]['content'])
		del(articles[index]['updated'])
		del(articles[index]['deleted'])

	article_arr = articles.pop(0)
	article_arr["site_title"]     = site_title
	article_arr["site_desc"]      = site_desc
	article_arr["site_domain"]    = site_domain
	article_arr["site_copyright"] = site_copyright
	article_arr["archives_url"]   = site_domain + "/archives.html"
	article_arr["recent_list"]    = articles
	article_arr["cate_list"]      = cates
	pa.createIndex(article_arr)
	# 生成分类列表页
	for _, notebook_row in enumerate(cates):
		notebook_guid = notebook_row['notebook_guid']
		note_list = da.fetchArticlesByCateGuid(notebook_guid)

		note_arr = {}
		note_arr["site_title"]     = site_title
		note_arr["site_desc"]      = site_desc
		note_arr["site_domain"]    = site_domain
		note_arr["site_copyright"] = site_copyright
		note_arr["note_list"]      = note_list
		note_arr['title']		   = notebook_row['name']
		note_arr["notebook_name"]  = notebook_row['name']
		note_arr["notebook_number"]= notebook_row['number']
		note_arr["cate_list"]      = cates

		pa.createCategory(notebook_guid, note_arr)
	# 生成归档列表
	note_arr = {}
	note_arr["site_title"]     = site_title
	note_arr["site_desc"]      = site_desc
	note_arr["site_domain"]    = site_domain
	note_arr["site_copyright"] = site_copyright
	note_arr["note_list"]      = note_list
	note_arr['title']		   = "最近归档文章"
	note_arr['note_list']      = da.fetchRecentItems(100)
	note_arr["number"]         = len(note_arr['note_list'])
	note_arr["cate_list"]      = cates
	pa.createArchives(note_arr)
