import asyncio
import websockets

@asyncio.coroutine
def hello(websocket, path):
    name = yield from websocket.recv()
    print("< {}".format(name))
    greeting = "Hello {}!".format(name)
    yield from websocket.send(greeting)
    print("> {}".format(greeting))

def launch_server(callback, ip='localhost', port='8001'):
	loop = asyncio.get_event_loop()
	coro = websockets.serve(callback, ip, port)
	ws_server = loop.run_until_complete(coro)
	print('Looking for connections on {}'.format(
	  ws_server.server.sockets[0].getsockname()))
	
	try:
		print("Press Control-C to stop the server.")
		loop.run_until_complete(do_nothing())
	except KeyboardInterrupt:
		logger.info("KeyboardInterrupt received: closing the server.")
	finally:
		ws_server.close()
		loop.run_until_complete(server.wait_closed())
		loop.close()

def do_nothing(seconds=1):
	"""Signals like the KeyboardInterrupt are not supported on windows. This workaround forces the event loop to 'check' for keyboard interrupts once a second. See http://bugs.python.org/issue23057"""
	while True:
		yield from asyncio.sleep(seconds)

if __name__ == "__main__":
	launch_server(hello)
