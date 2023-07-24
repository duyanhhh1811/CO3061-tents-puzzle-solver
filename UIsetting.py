from handle import *

# size, matrix, row, col = get_input()
# point_path = handle(size, matrix, row, col)

#  COLOR:
WHITE = (255,255,255)
BLACK = (0,0,0)
DARKGREY = (40,40,40)
LIGHTGREY = (100,100,100)
BGCOLOR = DARKGREY

TREE_COLOR = (187, 249, 187)
TENT_COLOR = (255, 243, 186)
CELL_COLOR = (212, 234, 183)
BG_COLOR = (217, 217, 219)
TEXT_COLOR = (42, 187, 83)

# ! Pastel color
# IVORY = (243, 227, 191)
# E8F1FD = (232, 241, 254)
F3E9EA = (243, 233, 234)
F3D0D4 = (243, 208, 212)
F2A7AC = (242, 167, 172)
F2A1C1 = (242, 161, 193)
F291A3 = (242, 145, 163)

STRONG_GREEN = (34, 121, 72)

GAMESIZE = int(input("CHOOSE SIZE (6 or 8): "))
if GAMESIZE == 6:
    TITLESIZE = 90
else: 
    TITLESIZE = 65

# GAME SETTING:
WIDTH = 1100
HEIGHT = 3000
FPS = 60
title = "Puzzle-tents"