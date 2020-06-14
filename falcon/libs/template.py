import re
"""
模板解析和变量分配
"""

class Template:

	def __init__(self, data):
		self.data = data

	#变量解析
	def parsing_var(self, var_name, var_value):
		if None == var_value: return
		if False == re.search("{{"+var_name+"}}", self.data): return
		self.data = self.data.replace("{{"+var_name+"}}", var_value)	

	# 列表字典解析
	def parsing_loop(self, var_name, var_value):
		pa = re.compile(r"\{\{loop\s+foreach\="+var_name+"\s+item=\S+.*\{\{\/loop\}\}", re.S)
		re_data  = re.findall(pa, self.data)
		raw_data = re_data[0]
		re_data  = re.findall(r"(\{\{loop\s+foreach\="+var_name+"\s+item=(\S+).*\}\})", raw_data)
		element_name = re_data[0][1]

		items = raw_data.split("\n")
		raw_element = "\n".join(items[1:-1])

		output_data = "";
		for row in var_value:
			item_data = raw_element.replace("{{","")
			item_data = item_data.replace("}}","")
			for element_key,element_val in row.items():
				item_data = item_data.replace(element_name+"."+element_key, element_val)

			output_data += item_data

		self.data = re.sub(pa, output_data, self.data)

	# 分配所有数据
	def assign(self, varss):
		for var_name, var_value in varss.items():
			if isinstance(var_value, list):
				self.parsing_loop(var_name, var_value)
			else:
				self.parsing_var(var_name, var_value)
		return self.data
""" 
if __name__ == "__main__":
	original_data ='''11111111111
		{{loop foreach=post_new_list item=item}}
		<div>
		{{item.createat}}
		<a href="{{item.url}}">{{item.subject}}</a>
		</div>
		{{/loop}}
		{{createat}}
		{{username}}
	'''

	varss = { 
		'post_new_list':[
			{'createat':"20200601",'url':"urldemo", "subject":"test subject"},
			{'createat':"20200602",'url':"urldemo2", "subject":"test subject2"},
		],
		'createat':"211111111111",
		'username':"genghonghao",
	}
	tp = Template(original_data)
	result_data = tp.assign(varss)
	print(result_data)
"""
