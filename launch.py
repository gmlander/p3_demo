import PySimpleGUIWeb as sg
from random import randint
import numpy as np
from time import sleep
from utils import Board

while True:
    h = 10
    w = 10
    board = Board(w, h)
    game_lost = False
    previous_display = board.display.copy()
    exited = False
    mines = board.num_mines
    mode_on = ('black','green')
    mode_off = ('black','red')
    clear_mode = True

    button_grid = [[sg.Button('?', size=(4, 2), key=(i,j),
                             pad=(0,0)) for j in range(w)] for i in range(h)]
    mode_toggle = [[sg.Text("Click Mode: "),
                  sg.Button('Mine', button_color = mode_off, key = 'mine_mode', pad = (0,0)),
                  sg.Button('Clear', button_color = mode_on, key = 'clear_mode', pad = (0,0))]]
    top_row =  [sg.Text("Mines Remaining:"), sg.Text(f"{mines}", pad = (50, 0),
                                                     text_color = 'red',
                                                     background_color='686463',
                                                    key = 'remaining'),
               sg.Column(mode_toggle)]
    layout = [top_row, *button_grid]
    window = sg.Window('Minesweeper', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            exited = True
            break

        if event in ('mine_mode', 'clear_mode'):
            clear_mode = event == 'clear_mode'
            window.FindElement('mine_mode').update(button_color = mode_off if clear_mode else mode_on)
            window.FindElement('clear_mode').update(button_color = mode_on if clear_mode else mode_off)        
            continue

        row, col = event[:2]
        
        if previous_display[row, col]:
            continue

        if not board.update_square(not clear_mode, row, col):
            game_lost = True
            display_diff = np.argwhere(board.display == board.display)
        else:
            mines -= not clear_mode
            if mines == 0:
                break
            display_diff = np.argwhere(previous_display != board.display)
            previous_display = board.display.copy()
            window.FindElement('remaining').update(mines)

        for x, y in display_diff:
            cell_val = board.board[x, y]

            if cell_val == -1:
                cell_val = '*'
                color_update = ('black','grey')
            elif cell_val == 0:
                cell_val = ' '
                color_update = ('white','black')
            else:
                color_update = ('white','black')

            window.FindElement((x, y)).update(cell_val, button_color=color_update)

        if game_lost:
            sleep(3)
            break

    if exited:
        break
            
    result = 'NURTZ!' if game_lost else 'HUZZAH!'
    if sg.PopupYesNo(result + '\nPlay again?') == 'No':
        break
window.close()