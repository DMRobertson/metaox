import asyncio
import json

@asyncio.coroutine
def transmit_message(socket, type, data):
	data['type'] = type
	enc = json.dumps(data)
	yield from socket.send(enc)
	return enc

@asyncio.coroutine
def await_message(socket):
	data = yield from socket.recv()
	if data is None:
		return
	data = json.loads(data)
	type = data['type']
	return type, data