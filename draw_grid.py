import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

from helpers import pad_binary
from encoding_mode import get_encoding_mode

''' Early Work
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

def draw_dark_module(grid):
    grid[14, 8] = 1


def draw_error_correction_level(grid, level='M'):
    """
    Super informative blog post: https://blog.qrstuff.com/2011/12/14/qr-code-error-correction
    """
    level = level.upper()
    if level == 'L':
        grid[8, 0], grid[8, 1] = 1, 1
        grid[19, 8], grid[20, 8] = 1, 1
    elif level == 'M':
        grid[8, 0] = 1
        grid[20, 8] = 1
    elif level == 'Q':
        grid[8, 1] = 1
        grid[19, 8] = 1
    elif level == 'H':
        pass
    else:
        raise ValueError(f"Value for level must be 'L', 'M', 'Q', or 'H'. You entered '{level}'.")


def draw_mask_pattern(grid, pattern_num=0):
    """
    Mask Pattern explainer: https://www.thonky.com/qr-code-tutorial/mask-patterns

    Mask Pattern 0: (row + column) % 2 == 0
    if the coordinates for a given bit match the above formula, switch the value of the bit.
    Question: What bits get considered, what bits do not?
    """
    """
    ## Not ready for prime-time
    if pattern_num > 7:
        raise ValueError(f"Mask pattern must be in range 0-7. You enetered '{pattern_num}'.")
    mask = bin(pattern_num)[2:]
    if pattern_num < 2:
        mask = '00' + mask
    elif pattern_num < 4:
        mask = '0' + mask
    grid[8, 4], grid[8, 3], grid[8, 2] = [int(digit) for digit in mask]
    grid[16, 8], grid[17, 8], grid[18, 8] = [int(digit) for digit in mask]
    """
    if pattern_num > 0:
        raise ValueError(f"Currently only mask pattern 0 is supported. You enetered '{pattern_num}'.")
    grid[8, 2], grid[8, 3], grid[8, 4] = 1, 0, 0
    grid[18, 8], grid[17, 8], grid[16, 8] = 1, 0, 0


def draw_mode_indicator(grid, data):
    """https://merricx.github.io/qrazybox/help/getting-started/about-qr-code.html"""
    grid[20, 20], grid[20, 19], grid[19, 20], grid[19, 19] = get_encoding_mode(data, verbose=False)


def draw_message_length(grid, data):
    padded_binary_string = pad_binary(bin(len(data)))
    binary_values = (int(digit) for digit in padded_binary_string)
    grid[18, 20], grid[18, 19], \
    grid[17, 20], grid[17, 19], \
    grid[16, 20], grid[16, 19], \
    grid[15, 20], grid[15, 19] = binary_values



print(v1_base_grid)
draw_finder_patterns(v1_base_grid)
draw_timing_patterns(v1_base_grid)
draw_dark_module(v1_base_grid)
draw_error_correction_level(v1_base_grid)
draw_mode_indicator(v1_base_grid, 'talzaken.com')
draw_mask_pattern(v1_base_grid)
print(v1_base_grid)
draw_message_length(v1_base_grid, 'talzaken.com')

# Plot and show the grid
cmap = colors.ListedColormap(['white', 'black'])
plt.imshow(v1_base_grid, cmap=cmap)
plt.show()