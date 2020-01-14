import tensorflow as tf
from tensorflow.keras import backend as K
from itertools import product
import os
import numpy as np

from model import create_model, input_fn

MINE_DIST = [0.65641, 0.23598, 0.05507, 0.01501, 0.00972, 0.00929, 0.00926, 0.00926]
MINE_COORDS = list(product(range(-1, 2), range(-1,2)))
SHOWN_COORDS = [c for c in MINE_COORDS if c != (0,0)]

def get_num_mines(s, mines, shown):

	if s in mines:
		return -1
	else:
		return sum([self.get_neighbor(*c) for c in product([x - 1, x, x + 1],
														[y - 1, y, y + 1])])

def good_neighbor(self, x, y):
	return (x >= 0 and x < self.w) and (y >= 0 and y < self.l)

def get_neighbor(self, x_adj, y_adj):
	return (x_adj, y_adj) in self.mines

def game_cell():
	num_mines = np.random.choice(a = [i for i in range(1,9)], p = MINE_DIST)
	mines = np.random.choice(a = MINE_COORDS,
							size = num_mines, replace = False)

	num_shown = np.random.choice(a = [i for i in range(9)])
	shown = np.random.choice(a = SHOWN_COORDS,
							size = num_shown, replace = False)

	cell = np.full((3,3), -2)

	for s in shown:
		cell[s] = get_num_mines(s, mines, shown)

	cell = cell.flatten()
	out_cell = np.delete(cell, 4)
	return out_cell