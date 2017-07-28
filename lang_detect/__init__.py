from get_lang import Command




def openfile(path):
	with open(path) as f:
		urls = f.readlines()
	return urls
	print urls


openfile()
for url in urls:
	search = Command.process_url(url)
	with open() as f:
		f.writelines(search)


