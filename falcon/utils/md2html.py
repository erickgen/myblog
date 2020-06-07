import codecs, markdown

def md2html(filename):
	input_file = codecs.open(filename, mode="r", encoding="utf-8")
	text = input_file.read()
	html = markdown.markdown(text)
	return html
