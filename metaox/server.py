import asyncio
import logging
import websockets
import re

from .client   import Client
from .config   import max_clients
from .game     import Game
from .protocol import await_command

extract_mark_args = re.compile(r'([012]\s*)' * 4 + '([12])')

class MetaOXServer:
	def __init__(self, ip='0.0.0.0', port='8001'):
		self.ip = ip
		self.port = port
		
		self.num_connections = 0
		self.loop = None
		
		self.clients = []
		self.game = Game()
	
	def launch(self):
		self.loop = asyncio.get_event_loop()
		start_server = websockets.serve(self.new_client, self.ip, self.port)
		server = self.loop.run_until_complete(start_server)
		logging.info('Looking for connections on {}:{}'.format(
		  self.ip, self.port))
		print("Press Control-C to stop the server.")
		try:
			self.loop.run_until_complete(do_nothing())
		except KeyboardInterrupt:
			logging.info("KeyboardInterrupt received: closing the server.")
		finally:
			server.close()
			self.loop.run_until_complete(server.wait_closed())
			self.loop.close()
	
	def add_task(self, coro):
		self.loop.create_task(coro)
	
	@asyncio.coroutine
	def new_client(self, socket, path):
		if len(self.clients) >= max_clients:
			return #discard connection TODO send an error message
		
		id = self.num_connections
		self.num_connections += 1
		c = Client(id, socket)
		logging.info("New client {}".format(c))
		
		self.clients.append(c)
		self.broadcast_client_names()
		self.broadcast_grids(only_client=c)
		
		while True:
			response = yield from await_command(socket)
			if response is None:
				break
			command, arg = response
			
			try:
				handler = getattr(self, 'handle_' + command)
			except AttributeError:
				logging.error("No handler for {} command from {}. Arg: {}".format(
				  command, c, arg))
			else:
				handler(c, arg)
		
		#When connection is lost:
		self.clients.remove(c)
		self.broadcast_client_names()
	
	#handlers for client commands
	def handle_edit_name(self, client, arg):
		client.name = arg
		yield from self.broadcast_client_names(except_for=client)
	
	def broadcast_client_names(self, except_for=None):
		data = {'client_names': [c.name for c in self.clients] }
		for i, c in enumerate(self.clients):
			if c is except_for:
				continue
			self.add_task(c.transmit_state(data))
			id = {'my_id' : i }
			self.add_task(c.transmit_state(id))
	
	def handle_mark(self, client, arg):
		#check it's this client's turn to mark
		
		match = extract_mark_args.match(arg.strip())
		if match is None:
			self.add_task(client.inform('Could not parse mark instruction'))
			return
		
		i, j, k, l = [int(x) for x in match.groups()]
		try:
			self.game.mark(i, j, k, l)
		except Exception as e:
			self.add_task(client.error(e))
		else:
			self.broadcast_grids(only_grid=(i, j))
	
	def broadcast_grids(self, only_grid=None, only_client=None):
		data = {}
		if only_grid is not None:
			data['grids'] = [self.game.dump_grid(*only_grid)]
		else:
			data['grids'] = [self.game.dump_grid(i, j) for i in range(3) for j in range(3)]
			
		data['metagrid'] = self.game.metagrid.dump()
		data['active'] = self.game.active_grid
		
		if only_client is not None:
			clients = [only_client]
		else:
			clients = self.clients
		for c in clients:
			self.add_task(c.transmit_state(data))
	
	def handle_say(self, client, arg):
		data = {'chat': '{}: {}'.format(client.name, arg) }
		for c in self.clients:
			self.add_task(c.transmit_state(data))

def do_nothing(seconds=1):
	"""Signals like the KeyboardInterrupt are not supported on windows. This workaround forces the event loop to 'check' for keyboard interrupts once a second. See http://bugs.python.org/issue23057"""
	while True:
		yield from asyncio.sleep(seconds)
