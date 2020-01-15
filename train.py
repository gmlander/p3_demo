# from itertools import product
# from collections import defaultdict
# import matplotlib.pyplot as plt

# import tensorflow as tf
# from tensorflow.keras import backend as K
# import os
# import numpy as np

# from utils import Board
# from model import create_model, input_fn

# MIN_X = 10
# MAX_X = 30
# MIN_Y = 10
# MAX_Y = 30
# NUM_BOARDS = 10
# OBS_PER_BOARD = 10

# # MINE_DIST = [0.65641, 0.23598, 0.05507, 0.01501, 0.00972, 0.00929, 0.00926, 0.00926]
# MINE_COORDS = list(product(range(-1, 2), range(-1,2)))
# SHOWN_COORDS = [c for c in MINE_COORDS if c != (0,0)]

# def build_train_data():

# 	game_feats = []
# 	game_cells = []
# 	cell_labels = []

# 	for i in range(MIN_X, MAX_X + 1):
# 	    for j in range(MIN_Y, MAX_Y + 1):
# 	        for _ in range(NUM_BOARDS):
# 	            board = Board(i, j)
# 	            squares = product(range(i), range(j))
# 	            cells = np.random.choice(squares, size = OBS_PER_BOARD, replace = False)
# 	            n_cells = board.w * board.l
# 	            n_mines = board.num_mines
# 	            for c in cells:

# 	            	cell = game_cell(board, c)
# 	                cell_mines = sum([1 for c in cell if c == -1])
# 	                cell_shown = sum([1 for c in cell if c >= 0])
# 	                mines_known = np.random.randint(cell_mines, n_mines - 1)
# 	                cells_known = np.random.randint(cell_shown, n_cells - 1)

# 	                # game state features
# 				    # total number of cells, total number of mines, number of known cells, number of known mines
# 				    game_feats.append((n_mines, n_cells, cells_known, mines_known))


# def game_cell(board, c):
# 	# num_mines = np.random.choice(a = [i for i in range(1,9)], p = MINE_DIST)
# 	# mines = np.random.choice(a = MINE_COORDS,
# 	# 						size = num_mines, replace = False)

# 	num_shown = np.random.randint(0, 9)
# 	shown = np.random.choice(a = SHOWN_COORDS,
# 							size = num_shown, replace = False)

# 	cell = np.full((3,3), -2)

# 	for s in shown:
# 		cell[s] = get_num_mines(s, mines, shown)

# 	cell = cell.flatten()
# 	out_cell = np.delete(cell, 4)
# 	return out_cell

# def get_num_mines(s, mines, shown):

# 	if s in mines:
# 		return -1
# 	else:
# 		x, y = s
# 		return sum([self.get_neighbor(*c) for c in product([x - 1, x, x + 1],
# 														[y - 1, y, y + 1])])