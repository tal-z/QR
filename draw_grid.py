import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
'''

"""
Mask Pattern: j % 2 = 0 
"""
version1_base_data = \
    [[1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
     [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
     [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # buf
     [1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # buf
     [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
     ]
print(version1_base_data)
cmap = colors.ListedColormap(['white', 'black'])

plt.imshow(version1_base_data, cmap=cmap)

plt.show()
'''

v1_base_grid = np.zeros((21, 21))

def draw_finder_patterns(grid):
    """fills in corners of grid with easily-recognized square QR pattern"""
    for i, row in enumerate(grid):
        for j, square in enumerate(row):
            # Draw horizontal outer lines
            if (i == 0 or i == 6 or i == 14 or i == 20) and (j < 7):
                grid[i, j] = 1
            if (i == 0 or i == 6) and (j > 14):
                grid[i, j] = 1
            # Draw vertical outer lines
            if (j == 0 or j == 6 or j == 14 or j == 20) and (i < 7):
                grid[i, j] = 1
            if (j == 0 or j == 6) and (i > 14):
                grid[i, j] = 1
            # Draw inner squares
            if (1 < i < 5) and (1 < j < 5):
                grid[i, j] = 1
            if (15 < i < 19) and (1 < j < 5):
                grid[i, j] = 1
            if (15 < j < 19) and (1 < i < 5):
                grid[i, j] = 1


def draw_timing_patterns(grid):
    """
    Fills in relevant area with evenly-spaced pattern of alternating black and white modules,
    used to tell the scanner the size of modules and the version of QR code being interpreted.
    This is the Version 1 timing pattern.
    """
    for i, row in enumerate(grid):
        for j, square in enumerate(row):
            if (i == 6) and (7 < j < 13) and (j % 2 == 0):
                grid[i, j] = 1
            if (j == 6) and (7 < i < 13) and (i % 2 == 0):
                grid[i, j] = 1



print(v1_base_grid)
draw_finder_patterns(v1_base_grid)
draw_timing_patterns(v1_base_grid)
print(v1_base_grid)



# Plot and show the grid
cmap = colors.ListedColormap(['white', 'black'])
plt.imshow(v1_base_grid, cmap=cmap)
plt.show()