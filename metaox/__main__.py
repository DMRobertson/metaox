'''launch with python -m metaox'''

if __name__ == "__main__":
	from .server import MetaOXServer
	MetaOXServer().launch()

'''todo serve the html files too'''