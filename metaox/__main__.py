'''launch with python -m metaox'''

if __name__ == "__main__":
	import logging
	from .server import MetaOXServer
	MetaOXServer().launch()

'''todo serve the html files too'''