from .grid import Cell, Grid

import random

class Game:
	def __init__(self):
		self.reset()
	
	def reset(self):
		self.grids = { (i, j) : Grid() for i in range(3) for j in range(3) }
		self.metagrid = Grid()
		self.turn = random.choice([Cell.player1, Cell.player2])
		x = random.randint(0, 8)
		self.active_grid = (x % 3, x // 3)
	
	def mark(self, i, j, k, l, value):
		if (i, j) != self.active_grid:
			raise KeyError('Cannot mark a non-active grid')
		if value != self.turn.value:
			raise ValueError('It is player {}\'s turn to mark.'.format(self.turn.value))
		grid = self.grids[i, j]
		grid.mark(k, l, value)
		self.active_grid = (k, l)
		
		result = grid.test_victory()
		if result != Cell.empty:
			self.metagrid.cells[i, j] = result
		return result
	
	def dump_grid(self, i, j):
		return [i, j] + self.grids[i, j].dump()