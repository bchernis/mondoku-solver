# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 23:20:56 2023

@author: boris

#Image processing tutorial: https://www.tutorialspoint.com/how-to-detect-a-rectangle-and-square-in-an-image-using-opencv-python

To Do
-Check that number of columns is consistent for each row
-Remove debugging stuff
-Maybe it's possible to NOT start from scratch with each iteration? Irrelevant performance-wise unless board is very large.
-Maybe make colors start from 0
"""

import numpy as np

n_colors = 6
n_rows = 11
n_cols = 9

# Coordinates and color of each rectangle
rects = {(0, 0, 0, 0): 0,
              (0, 1, 1, 1): 4,
              (0, 2, 2, 3): 1,
              (0, 4, 0, 4): 3,
              (0, 5, 2, 7): 0,
              (0, 8, 2, 8): 5,
              (1, 0, 1, 0): 3,
              (1, 4, 2, 4): 0,
              (2, 0, 3, 0): 0,
              (2, 1, 2, 1): 0,
              (3, 1, 3, 2): 2,
              (3, 3, 3, 3): 0,
              (3, 4, 4, 6): 1,
              (3, 7, 3, 7): 3,
              (3, 8, 3, 8): 6,
              (4, 0, 4, 1): 0,
              (4, 2, 4, 2): 0,
              (4, 3, 5, 3): 3,
              (4, 7, 4, 7): 2,
              (4, 8, 4, 8): 0,
              (5, 0, 7, 1): 0,
              (5, 2, 7, 2): 6,
              (5, 4, 6, 5): 5,
              (5, 6, 6, 7): 4,
              (5, 8, 5, 8): 2,
              (6, 3, 6, 3): 0,
              (6, 8, 7, 8): 0,
              (7, 3, 7, 4): 4,
              (7, 5, 8, 5): 2,
              (7, 6, 7, 7): 5,
              (8, 0, 10, 1): 5,
              (8, 2, 9, 2): 0,
              (8, 3, 10, 4): 0,
              (8, 6, 8, 6): 0,
              (8, 7, 10, 8): 1,
              (9, 5, 9, 5): 3,
              (9, 6, 10, 6): 2,
              (10, 2, 10, 2): 3,
              (10, 5, 10, 5): 0}


def compute_bool_map():
    bool_map = np.ones((n_colors, n_rows, n_cols), dtype=bool)
    
    # No square can have two colors, and no two squares on the same
    # row or column can have the same color
    for rect, color in rects.items():
        row_min, col_min, row_max, col_max = rect
        color_index = color - 1
        if color > 0:
            bool_map[:, row_min:row_max+1, col_min:col_max+1] = False
            bool_map[color_index, :, col_min:col_max+1] = False
            bool_map[color_index, row_min:row_max+1, :] = False
            
    # If any square of a rectangle is ruled out for a color, so is the entire rectangle
    for rect, color in rects.items():
        if color == 0:
            for color_index in range(n_colors):
                row_min, col_min, row_max, col_max = rect
                if False in bool_map[color_index, row_min:row_max+1, col_min:col_max+1]:
                    bool_map[color_index, row_min:row_max+1, col_min:col_max+1] = False
    return bool_map

def find_rect(row, col):
    for rect in rects.keys():
        row_min, col_min, row_max, col_max = rect
        if row >=row_min and row <= row_max and col >= col_min and col <= col_max:
            return rect

def add_rect():
    bool_map_sum = np.sum(bool_map, axis=0)
    for row in range(n_rows):
        for col in range(n_cols):
            if bool_map_sum[row, col] == 1:
                for color_index in range(n_colors):
                    if bool_map[color_index, row, col]:
                        rects[find_rect(row, col)] = color_index + 1
                        return
    
def print_solution():
   board = np.zeros((n_rows, n_cols))
   for rect, color in rects.items():
       row_min, col_min, row_max, col_max = rect
       board[row_min:row_max+1, col_min:col_max+1] = color
   print(board)
    
bool_map = compute_bool_map()

while True in bool_map:
    add_rect()
    bool_map = compute_bool_map()

print_solution()