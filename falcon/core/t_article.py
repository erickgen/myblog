#-*- coding:utf-8 -*-
from libs.TemplateParsing import TemplateParsing

theme_name = "default"

article = {
	"site_title":"中子星金融",
	"site_desc":"努力工作，努力生活，记录美好生活！",
	"site_domain":"https://xingyoucai.com",
	"blog_guid":"xxxxxxxxxxxx11111",
	"blog_subject":"测试标题",
	"blog_author":"测试标题",
	"blog_content":"测试内容0000001",
	"blog_created":"2020-05-22",
	"updated":"2020-05-22",
	"cate_name":"测试分类",
	"cate_url":"/archives/aaaaaaaiiiii.html",
	"copyright_info":"京ICP 3000011111",
	"previous_url":"/aaaaaaaa.html",
	"previous_subject":"xxxxxxxxxxxxxxxxxx",
	"next_url":"/aaaaaaaaafffffff.html",
	"next_subject":"dddddiiiiiii",
}

def createFile(filename, content):
	fp = open(filename, 'w')
	fp.write(content)
	fp.close()

# 详情页
with open('./template/'+theme_name+'/detail.html') as read_file: detail_html = read_file.read()
tp   = TemplateParsing(detail_html)
html = tp.assign(article)
detail_file = "./wwwroot/archives/"+article["blog_guid"]+".html"
createFile(detail_file, html)
# 最新文章20条, 更新一条，删除一条
# 分类文章数据
# 更新更多文章列表页
# 生成文章分类页
# 生产首页
# 更新统计数据
