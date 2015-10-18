import asyncio
import logging

from .protocol import transmit_state

class Client:
	def __init__(self, id, socket):
		self.id = id
		self.socket = socket
		self.name = "client {} ({})".format(id, self.socket.host)
	
	def __str__(self):
		return 'Client #{} ({}) at {}:{}'.format(
		  self.id, self.name, self.socket.host, self.socket.port) 
	
	def transmit_state(self, data):
		enc = yield from transmit_state(self.socket, data)
		logging.debug('-> {} ({}): {}'.format(
		  self.id, self.name, enc))