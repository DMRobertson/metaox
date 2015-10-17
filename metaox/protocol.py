import asyncio
import json

@asyncio.coroutine
def transmit_message(socket, type, data):
	data['type'] = type
	enc = json.dumps(data)
	yield from socket.send(enc)
	return enc