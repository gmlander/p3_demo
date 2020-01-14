import numpy as np
from itertools import product

class Board():

	def __init__(self, l, w = None):
		self.w = w or l
		self.l = l
		self.num_mines = max(self.w*self.l // 10, 1)
		self.board = np.empty((self.w,self.l), dtype = np.int16)

		locations = list(product(range(self.w), range(self.l)))
		mine_ix = np.random.choice(range(len(locations)), size = self.num_mines, replace = False)
		self.mines = [locations[ix] for ix in mine_ix]

		for x in range(self.w):
			for y in range(self.l):
				self.board[x][y] = self.get_num_mines(x,y)

		self.display = np.zeros((self.w, self.l), dtype = bool)

	def get_num_mines(self, x, y):
		if (x,y) in self.mines:
			return -1
		else:
			return sum([self.get_neighbor(*c) for c in product([x - 1, x, x + 1],
															[y - 1, y, y + 1])])

	def good_neighbor(self, x, y):
		return (x >= 0 and x < self.w) and (y >= 0 and y < self.l)

	def get_neighbor(self, x_adj, y_adj):
		return (x_adj, y_adj) in self.mines

	def update_square(self, pick_mine, x, y):
		if (x,y) in self.mines:
			if pick_mine:
				self.display[x][y] = True
				return True
			else:
				return False
		else:
			if pick_mine:
				return False
			else:
				self.update_adjacents(x,y)
				return True

	def update_adjacents(self, x, y):
		'''recursively frees up display on adjacent squares when clear
		cell is selected'''
		if self.board[x][y] == 0:
			self.display[x][y] = True
			for cx, cy in product([x - 1, x, x + 1],[y - 1, y, y + 1]):
				if self.good_neighbor(cx, cy):
					if not self.display[cx][cy]:
						self.display[cx][cy] = True
						if self.board[cx][cy] == 0:
							_ = self.update_adjacents(cx, cy)
			return True

		else:
			self.display[x][y] = True
			return False