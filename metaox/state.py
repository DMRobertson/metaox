import json
from random import randrange, randint

def reset_state():
	state = {
		'board': [0 for k in range(3) for l in range(3) for i in range(3) for j in range(3)],
		'grids': [0 for k in range(3) for l in range(3)],
		'active': (randrange(3) , randrange(3)),
		'player': randint(1, 2),
	}
	return state

