<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<meta name="author" content="David Robertson" />
		<script type="text/javascript" src="script.js"></script>
		<title>Metaox</title>
		
		<!-- Bootstrap core CSS -->
		<link rel="stylesheet" href="css/bootstrap.min.css" />
		<link rel="stylesheet" href="css/styles.css" />
		
		<!-- HTML5 shiv and Respond.js for IE8 support of HTML5 elements and media queries -->
		<!--[if lt IE 9]>
		<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
		<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->
	</head>
	<body>
		<main>
			<table id="metagrid">
				{% for i in range(3) %}
				<tr>
					{% for j in range(3) %}
					<td>
						<table class="grid row{{i}} col{{j}}" id="grid{{i}}{{j}}">
							{% for k in range(3) %}
							<tr>
								{% for l in range (3) %}
								<td class="cell row{{k}} col{{l}}" id="cell{{i}}{{j}}{{k}}{{l}}"></td>
								{% endfor %}
							</tr>
							{% endfor %}
						</table>
					</td>
					{% endfor %}
				</tr>
				{% endfor %}
			</table>
		</main>
		<aside>
			<ul id="clients">
				{% for i in range(config['max_clients'])%}
				<li class="unused"><input type="text" id="client{{i}}" /></li>
				{% endfor %}
			</ul>
			<ul id="log">
			</ul>
			<input type="text" id="chat" />
		</aside>
	</body>
</html>
