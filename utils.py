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

	def get_num_mines(self, x, y):
		if (x,y) in self.mines:
			return -1
		else:
			return sum([self.get_neighbor(*c) for c in product([x - 1, x, x + 1],
															[y - 1, y, y + 1])])

	def get_neighbor(self, x_adj, y_adj):
		if x_adj < 0 or y_adj < 0:
			return 0
		elif x_adj >= self.w or y_adj >= self.l:
			return 0
		else:
			return (x_adj, y_adj) in self.mines