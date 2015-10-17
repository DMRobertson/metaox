import asyncio
import logging

from .protocol import transmit_message

class Client:
	def __init__(self, id, socket):
		self.id = id
		self.socket = socket
		self.name = "client {}".format(id)
	
	def __str__(self):
		return 'Client #{} ({}) at {}:{}'.format(
		  self.id, self.name, self.socket.host, self.socket.port) 
	
	def send_message(self, type, data):
		enc = yield from transmit_message(self.socket, type, data)
		logging.debug('-> {} ({}): {}'.format(
		  self.id, self.name, enc))