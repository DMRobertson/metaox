from enum import IntEnum

class Cell(IntEnum):
	empty   = 0
	player1 = 1
	player2 = 2
	drawn   = 3

class Grid:
	def __init__(self):
		self.reset()
	
	def __str__(self):
		return ''.join(str(self.cells[k, l].value) for k in range(3) for l in range(3) )
	
	def reset(self):
		self.cells = { (k, l) : Cell.empty for k in range(3) for l in range(3) }
	
	def mark(self, x, y, value):
		if self.cells[x, y] != Cell.empty:
			raise ValueError('Invalid: this cell is already marked.')
		#else
		self.cells[x, y] = Cell(value)
		return self.cells[x, y]
	
	def test_victory(self):
		#None for no outcome; 1 or 2 for victory to player 1 or 2; 0 for a full grid ending in a draw
		#verticals first
		for k in range(3):
			if self.cells[k, 0] == self.cells[k, 1] == self.cells[k, 2] != Cell.empty:
				return self.cells[k, 0]
		
		#horizontals
		for l in range(3):
			if self.cells[0, l] == self.cells[1, l] == self.cells[2, l] != Cell.empty:
				return self.cells[0, l]
		
		#diagonals
		if self.cells[0, 0] == self.cells[1, 1] == self.cells[2, 2] != Cell.empty:
			return self.cells[0, 0]
		if self.cells[2, 0] == self.cells[1, 1] == self.cells[0, 2] != Cell.empty:
			return self.cells[2, 0]
		
		#check for full grid
		num_marked = sum(cell != Cell.empty for cell in self.cells.values())
		if num_marked == 9:
			return Cell.drawn
		#otherwise, grid unfinished
		return Cell.empty
	
	def dump(self):
		return [self.cells[k, l].value for k in range(3) for l in range(3)]