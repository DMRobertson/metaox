import asyncio
import websockets

from .state import encode_message, reset_state

class MetaOXServer:
	def __init__(self, ip='localhost', port='8001'):
		self.ip = ip
		self.port = port
		self.connection_queue = asyncio.Queue()
		self.num_connections = 0
		
		self.games = {}
		self.num_games = 0
	
	def launch(self):
		loop = asyncio.get_event_loop()
		start_server = websockets.serve(self.connection_established, self.ip, self.port)
		try:
			ws_server = loop.create_task(start_server)
			loop.create_task(self.matchmaker())
			print('Looking for connections on {}:{}'.format(
			  self.ip, self.port))
			print("Press Control-C to stop the server.")
			loop.run_until_complete(do_nothing())
			
		except KeyboardInterrupt:
			print("KeyboardInterrupt received: closing the server.")
	
	@asyncio.coroutine
	def connection_established(self, socket, path):
		id = self.num_connections
		self.num_connections += 1
		print("Connection #{} from {} to {}".format(
		  id, format_socket(socket), path))
		yield from self.connection_queue.put((socket, path))
	
	@asyncio.coroutine
	def matchmaker(self):
		while True:
			socket1, path1 = yield from self.connection_queue.get()
			assert path1 == '/'
			socket2, path2 = yield from self.connection_queue.get()
			assert path2 == '/'
			#todo: decide how to handle paths
			game = Game(self.num_games, socket1, socket2)
			self.games[self.num_games] = game
			self.num_games += 1

def format_socket(socket):
	return '{}:{}'.format(socket.host, socket.port)

def do_nothing(seconds=1):
	"""Signals like the KeyboardInterrupt are not supported on windows. This workaround forces the event loop to 'check' for keyboard interrupts once a second. See http://bugs.python.org/issue23057"""
	while True:
		yield from asyncio.sleep(seconds)
