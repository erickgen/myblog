# main.py
# -*- coding: utf-8 -*-
import configparser
import sys
import time

sys.path.append(r"./libs/evernotesdk/lib")
import hashlib
import binascii
import os
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter

from utils.mytime import formatDate
from utils.string import xml2Html

class Note:
	def __init__(self, config_file):
		self.conf = configparser.ConfigParser(allow_no_value=True)
		self.conf.read(config_file)
		sandbox = self.conf.get("env", "sandbox")
		china   = self.conf.get("env", "china")
		if 'True' == sandbox:
			auth_token = self.conf.get("yinxiang", "devtoken")
		else:
			auth_token = self.conf.get("yinxiang", "prodtoken")
		self.client = EvernoteClient(token=auth_token, sandbox=sandbox, china=china)

	def check(self):
		user_store = self.client.get_user_store()
		version_ok = user_store.checkVersion(
			"Evernote EDAMTest (Python)",
			UserStoreConstants.EDAM_VERSION_MAJOR,
			UserStoreConstants.EDAM_VERSION_MINOR
		)
		if not version_ok: 
			#调用的不是印象云笔记API的最新版本,程序终止执行。", str(version_ok)
			return False
		return True

	def getsNoteBooks(self):
		self.note_store = self.client.get_note_store()
		# 取配置的分类
		notebooks = self.note_store.listNotebooks()
		notebookname = self.conf.get("env", "notebook")
		notebook_names = notebookname[1:-1].replace("'","").replace('"',"").split(",")

		notebook_guids = {}
		for notebook in notebooks:
			if notebook.name in notebook_names : notebook_guids[notebook.guid] = notebook.name

		self.notebook_guids = notebook_guids

	def getsContent(self, limit):
		self.getsNoteBooks()
		# 取最近4条笔记
		article_list = {}
		for guid, _  in self.notebook_guids.items():
			searchfilter = NoteFilter(notebookGuid=guid)
			offset       = 0
			article_list[guid] = self.note_store.findNotes(searchfilter, offset, limit)

		if not bool(article_list):
			#print(notebookname+"的笔记本中没有数据")
			return False

		return_data = []
		for notebook_guid, notebook_article in article_list.items():
			for row in notebook_article.notes:
				data = {}
				if True != row.active: continue
				data["deleted"] = row.deleted # None or True
				data["guid"] = row.guid
				data["title"] = row.title
				data["content"] = row.content
				data["created"] = formatDate(row.created)
				data["updated"] = formatDate(row.updated)
				content = self.note_store.getNoteContent(row.guid)
				content = xml2Html(content)
				data["notebook_guid"] = notebook_guid 
				data["notebook_name"] = self.notebook_guids[notebook_guid]
				data["content"] = content
				return_data.append(data)

				if None != row.resources:
					for image in row.resources:
						suffix = image.mime[image.mime.find("/")+1:]
						'''
						print(image.width)
						print(image.height)
						'''
						#生成图片
						binary_data = self.note_store.getResourceData(image.guid)
						file_name = hashlib.md5(binary_data).hexdigest()
						file_path = "./html/upload/"+file_name + "." + suffix
						image = open(file_path,'wb')
						image.write(bytes(binary_data))
						image.close()
		return_data = sorted(return_data, key=lambda keys:keys['created'], reverse=True)
		return return_data
