"""
按分类存储文件
"""
a = {
	"guidkey01":{
		"cate_name":"测试分类",
		"articles":{
			[
			{"guid":"aabbbccdd", "created":"2020-09-09", "title":"测试标题0000001"},
			{"guid":"aabbbccddcc", "created":"2020-09-08", "title":"测试标题0000002"},
			]	
		}
	}
}

#以json格式写入文件
def createFile(fileName, inData):
    with open(fileName, "w") as fp: fp.write(json.dumps(inData, indent=4, ensure_ascii=False))

# 读取Json数据
def readFile(fileName):
    if False == os.path.exists(fileName):
        return False
    with open(fileName,'r') as load_f: load_dict=json.load(load_f)
    return load_dict


# 月度文章

# 年底文章
