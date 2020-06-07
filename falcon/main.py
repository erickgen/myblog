from core.note import Note

if __name__ == "__main__":
	note  = Note("./config.ini")
	notes = note.getsContent()
	print(notes)
