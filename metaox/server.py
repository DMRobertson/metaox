import asyncio
import logging
import websockets

from .client import Client
from .config import max_clients

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
		id = self.num_connections
		self.num_connections += 1
		c = Client(id, socket)
		logging.info("New client {}".format(c))
		
		self.clients.append(c)
		self.loop.create_task(self.broadcast_client_names())
		
		while True:
			x = yield from socket.recv()
			if x is None:
				break
			else:
				... #handle x
		
		#When connection is lost:
		self.clients.remove(c)
		self.loop.create_task(self.broadcast_client_names())
	
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
