import asyncio
import json

@asyncio.coroutine
def transmit_state(socket, state):
	enc = json.dumps(state)
	yield from socket.send(enc)
	return enc

@asyncio.coroutine
def await_command(socket):
	message = yield from socket.recv()
	if message is None:
		return
	command, arg = message.split(' ', 1)
	return command, arg