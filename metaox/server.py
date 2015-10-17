import asyncio
import logging
import websockets

from .client   import Client
from .config   import max_clients
from .protocol import await_message

class MetaOXServer:
	def __init__(self, ip='localhost', port='8001'):
		self.ip = ip
		self.port = port
		self.clients = []
		self.num_connections = 0
		self.loop = None
	
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
	
	@asyncio.coroutine
	def new_client(self, socket, path):
		if len(self.clients) >= max_clients:
			return #discard connection TODO send an error message
		
		id = self.num_connections
		self.num_connections += 1
		c = Client(id, socket)
		logging.info("New client {}".format(c))
		
		self.clients.append(c)
		self.loop.create_task(self.broadcast_client_names())
		
		while True:
			response = yield from await_message(socket)
			if response is None:
				break
			type, data = response
			
			try:
				handler = getattr(self, 'handle_' + type)
			except AttributeError:
				logging.error("Unable to handle {} message. Data: {}".format(
				  type, data))
			else:
				yield from handler(c, data)
		
		#When connection is lost:
		self.clients.remove(c)
		self.loop.create_task(self.broadcast_client_names())
	
	@asyncio.coroutine
	def handle_edit_name(self, client, data):
		client.name = data['name']
		yield from self.broadcast_client_names()
	
	@asyncio.coroutine
	def broadcast_client_names(self):
		data = {'clients': [c.name for c in self.clients] }
		for i, c in enumerate(self.clients):
			data['my_id'] = i
			yield from c.send_message('client_names', data)

def do_nothing(seconds=1):
	"""Signals like the KeyboardInterrupt are not supported on windows. This workaround forces the event loop to 'check' for keyboard interrupts once a second. See http://bugs.python.org/issue23057"""
	while True:
		yield from asyncio.sleep(seconds)
