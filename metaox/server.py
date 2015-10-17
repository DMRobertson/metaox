import asyncio
import websockets

from queue import Queue

from .state import encode_message, reset_state

class MetaOXServer:
	def __init__(self, ip='localhost', port='8001'):
		self.ip = ip
		self.port = port
		self.queue = Queue()
		self.num_connections = 0
	
	def launch(self):
		loop = asyncio.get_event_loop()
		coro = websockets.serve(self.connection_established, self.ip, self.port)
		ws_server = loop.run_until_complete(coro)
		print('Looking for connections on {}'.format(
		  ws_server.server.sockets[0].getsockname()))
		
		try:
			print("Press Control-C to stop the server.")
			loop.run_until_complete(do_nothing())
		except KeyboardInterrupt:
			print("KeyboardInterrupt received: closing the server.")
		finally:
			ws_server.close()
			loop.run_until_complete(ws_server.wait_closed())
			loop.close()
	
	@asyncio.coroutine
	def connection_established(self, socket, path):
		id = self.num_connections
		self.num_connections += 1
		print("Connection #{id} from {socket.host}:{socket.port} to {path}".format(
		  id=id, socket=socket, path=path))
		yield from socket.send(encode_message('state', reset_state()))

def do_nothing(seconds=1):
	"""Signals like the KeyboardInterrupt are not supported on windows. This workaround forces the event loop to 'check' for keyboard interrupts once a second. See http://bugs.python.org/issue23057"""
	while True:
		yield from asyncio.sleep(seconds)

if __name__ == "__main__":
	MetaOXServer().launch()

'''todo serve the html files too'''