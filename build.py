from jinja2 import Environment, FileSystemLoader
import os
import metaox.config

env = Environment(
	loader=FileSystemLoader('.'),
	lstrip_blocks = True,
	trim_blocks   = True,
)
template = env.get_template('index.tpl')

with open("index.html", "wt") as f:
	document = template.render(config=metaox.config);
	f.write(document)

os.system('sass css/styles.scss css/styles.css')