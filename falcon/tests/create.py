# create.py
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


conf = configparser.ConfigParser(allow_no_value=True)
conf.read("./conf/site.ini")
auth_token = conf.get("yinxiang", "developertoken")

sandbox = True
china   = True

client = EvernoteClient(token=auth_token, sandbox=sandbox,china=china)

user_store = client.get_user_store()
note_store = client.get_note_store()

notebooks = note_store.listNotebooks()
print("Found ", len(notebooks), " notebooks:")
guid = None
for notebook in notebooks:
    print("  * ", notebook.name)
    if None == guid: guid = notebook.guid

# 生成文章
noteBody = "测试文章节内容ABCDEFG"
nBody = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
nBody += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
nBody += "<en-note>%s</en-note>" % noteBody

note = Types.Note()
note .title = "这是一个测试标题"
note.content = nBody
note.notebookGuid = guid

created_note = note_store.createNote(note)

print("Successfully created a new note with GUID: ", created_note.guid)
