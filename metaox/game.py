
class Game:
	def __init__(self, id, p1, p2):
		print("Starting game #{}: {} versus {}".format(
		  id, format_socket(p1), format_socket(p2)))
		self.state = reset_state()
		self.id = id
		self.p1 = p1
		self.p2 = p2