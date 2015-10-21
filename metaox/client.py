import asyncio
import logging
from socket import gethostbyaddr
import re

from .protocol import transmit_state

extract_host_name = re.compile(r'(\w+)(?:\.campus)?\.ncl\.ac\.uk')

class Client:
	def __init__(self, id, socket):
		#todo allow the client to provide their own name upon connection (cookie)
		self.id = id
		self.socket = socket
		dns_name = gethostbyaddr(socket.remote_address[0])[0].lower()
		match = extract_host_name.match(dns_name)
		if match:
			self.name = match.groups()[0]
		else:
			self.name = dns_name
	def __str__(self):
		return 'Client #{} ({})'.format(
		  self.id, self.name) 
	
	@asyncio.coroutine
	def transmit_state(self, data):
		enc = yield from transmit_state(self.socket, data)
		logging.debug('-> {} ({}): {}'.format(
		  self.id, self.name, enc))
	
	@asyncio.coroutine
	def inform(self, message):
		yield from self.transmit_state({'info': message})
	
	@asyncio.coroutine
	def error(self, message):
		if isinstance(message, Exception):
			message = ";".join(arg for arg in message.args)
		yield from self.transmit_state({'error': message})
