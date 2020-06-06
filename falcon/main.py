# main.py
# -*- coding: utf-8 -*-
import configparser
import sys
import time
import re

sys.path.append(r"./evernotesdk/lib")

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
import os
from evernote.api.client import EvernoteClient

from evernote.edam.notestore.ttypes import NoteFilter

from libs.utils import formatDate,convertBool
from libs.data  import getLatestArticleFlag


conf = configparser.ConfigParser(allow_no_value=True)
conf.read("./conf/site.ini")
sandbox = convertBool(conf.get("env", "sandbox"))
china   = convertBool(conf.get("env", "china"))

if True == sandbox:
	auth_token = conf.get("yinxiang", "devtoken")
else:
	auth_token = conf.get("yinxiang", "prodtoken")

client = EvernoteClient(token=auth_token, sandbox=sandbox,china=china)

user_store = client.get_user_store()

version_ok = user_store.checkVersion(
    "Evernote EDAMTest (Python)",
    UserStoreConstants.EDAM_VERSION_MAJOR,
    UserStoreConstants.EDAM_VERSION_MINOR
)

if not version_ok: 
	print("调用的不是印象云笔记API的最新版本,程序终止执行。", str(version_ok))
	exit(1)

note_store = client.get_note_store()

# 取配置的分类
notebooks = note_store.listNotebooks()
notebookname = conf.get("env", "notebook")
notebook_names = notebookname[1:-1].replace("'","").replace('"',"").split(",")

notebook_guids = {}
for notebook in notebooks:
	if notebook.name in notebook_names : notebook_guids[notebook.guid] = notebook.name

# 取最近4条笔记
article_list = {}
for guid,_  in notebook_guids.items():
	searchfilter = NoteFilter(notebookGuid=guid)
	offset       = 0
	maxnotes     = 8
	article_list[guid] = note_store.findNotes(searchfilter, offset, maxnotes)

if not bool(article_list):
	print(notebookname+"的笔记本中没有数据")
	exit(1)

# 找到最后更新的guid
latestflag = getLatestArticleFlag(conf.get("path", "latestflag"))
over_loop = False

def xml2Html(xml_content):
	html = xml_content.split("<en-note>")[1].replace("</en-note>", "")
	pa1 = re.compile(r"\<en\-media.*\s+hash\=\"[0-9a-z+]+\".*\<\/en\-media\>", re.M)
	re_data1  = re.findall(pa1, html)

	pa2 = re.compile(r"\<en\-media.*\s+hash\=\"[0-9a-z+]+\"/\>", re.M)
	re_data2  = re.findall(pa2, html)

	match_items = re_data1 + re_data2;
	for row in match_items:
		img = row.split("hash=")[1].split('"')[1]
		element_image = "<img src='/upload/"+img+".png'/>"
		html = html.replace(row, element_image)
	return html

for notebook_guid, notebook_article in article_list.items():
	if True == over_loop: break;
	for row in notebook_article.notes:
		if latestflag == row.guid: 
			over_loop = True
			break
		data = {}
		data["guid"] = row.guid
		data["title"] = row.title
		data["content"] = row.content
		data["created"] = formatDate(row.created)
		data["updated"] = formatDate(row.updated)
		content = note_store.getNoteContent(row.guid)
		content = xml2Html(content)
		print(content)

		if None != row.resources:
			for image in row.resources:
				suffix = image.mime[image.mime.find("/")+1:]
				print(image.width)
				print(image.height)
				#生成图片
				binary_data = note_store.getResourceData(image.guid)
				file_name = hashlib.md5(binary_data).hexdigest()
				file_path = "./wwwroot/upload/"+file_name + "." + suffix
				image = open(file_path,'wb')
				image.write(bytes(binary_data))
				image.close()
