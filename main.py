# main.py
# -*- coding: utf-8 -*-
import configparser
import sys
import time

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

notebooks = note_store.listNotebooks()
notebookname = conf.get("env", "notebook")
notebookguid = None
for notebook in notebooks:
    if notebookname == notebook.name: notebookguid = notebook.guid

# 取最近4条笔记
searchfilter = NoteFilter(notebookGuid=notebookguid)
offset       = 0
maxnotes     = 4
articlelist = note_store.findNotes(searchfilter, offset, maxnotes)

if None == articlelist:
	print(notebookname+"的笔记本中没有数据")
	exit(1)


# 找到最后更新的guid
latestflag = getLatestArticleFlag(conf.get("path", "latestflag"))

if latestflag == articlelist.notes[0].guid and latestflag != None:
	print("没有新数据需要更新")
	exit(1)

for row in articlelist.notes:
	data = {}
	data["guid"] = row.guid
	data["title"] = row.title
	data["content"] = row.content
	data["created"] = formatDate(row.created)
	data["updated"] = formatDate(row.updated)
	content = note_store.getNoteContent(row.guid)
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
