import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

from helpers import pad_binary, bitstring_to_bytes
from encoding_mode import get_encoding_mode
from latin1_to_binary import encode_data
from error_correction import generate_code_words


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


def draw_data(grid, data):
    """
    update matrix with data from encoded bitstring.
    This includes encoding type and data length,
    but not the error correction codewords.

    :param grid:
    :param data:
    :return:
    """

    coords_dict = {
        '0': [(20, 20), (20, 19), (19, 20), (19, 19), (18, 20), (18, 19), (17, 20), (17, 19)],
        '1': [(16, 20), (16, 19), (15, 20), (15, 19), (14, 20), (14, 19), (13, 20), (13, 19)],
        '2': [(12, 20), (12, 19), (11, 20), (11, 19), (10, 20), (10, 19), (9, 20), (9, 19)],
        '3': [(9, 18), (9, 17), (10, 18), (10, 17), (11, 18), (11, 17), (12, 18), (12, 17)],
        '4': [(13, 18), (13, 17), (14, 18), (14, 17), (15, 18), (15, 17), (16, 18), (16, 17)],
        '5': [(17, 18), (17, 17), (18, 18), (18, 17), (19, 18), (19, 17), (20, 18), (20, 17)],
        '6': [(20, 16), (20, 15), (19, 16), (19, 15), (18, 16), (18, 15), (17, 16), (17, 15)],
        '7': [(16, 16), (16, 15), (15, 16), (15, 15), (14, 16), (14, 15), (13, 16), (13, 15)],
        '8': [(12, 16), (12, 15), (11, 16), (11, 15), (10, 16), (10, 15), (9, 16), (9, 15)],
        '9': [(9, 14), (9, 13), (10, 14), (10, 13), (11, 14), (11, 13), (12, 14), (12, 13)],
        '10': [(13, 14), (13, 13), (14, 14), (14, 13), (15, 14), (15, 13), (16, 14), (16, 13)],
        '11': [(17, 14), (17, 13), (18, 14), (18, 13), (19, 14), (19, 13), (20, 14), (20, 13)],
        '12': [(20, 12), (20, 11), (19, 12), (19, 11), (18, 12), (18, 11), (17, 12), (17, 11)],
        '13': [(16, 12), (16, 11), (15, 12), (15, 11), (14, 12), (14, 11), (13, 12), (13, 11)],
        '14': [(12, 12), (12, 11), (11, 12), (11, 11), (10, 12), (10, 11), (9, 12), (9, 11)],
        '15': [(8, 12), (8, 11), (7, 12), (7, 11), (5, 12), (5, 11), (4, 12), (4, 11)],
    }
    bitstring = encode_data(data)
    encoded_data = bitstring_to_bytes(bitstring)

    for i in range(16):
        coords = coords_dict[str(i)]
        bits = encoded_data[i]
        for bit, coord in zip(bits, coords):
            grid[coord] = bit







# Update the QR Code
draw_finder_patterns(v1_base_grid)
draw_timing_patterns(v1_base_grid)
draw_dark_module(v1_base_grid)
#draw_error_correction_level(v1_base_grid)
#draw_mode_indicator(v1_base_grid, 'talzaken.com')
#draw_mask_pattern(v1_base_grid)
#draw_message_length(v1_base_grid, 'talzaken.com')

draw_data(v1_base_grid, 'talzaken.com')


# Plot and show the QR Code
fig, ax = plt.subplots()
cmap = colors.ListedColormap(['white', 'black'])
for i in range(0,21):
    plt.vlines(i-.5, -.5, 20.5)
    plt.hlines(i-.5, -.5, 20.5)
plt.imshow(v1_base_grid, cmap=cmap)
ax.set_xticks(range(0, 21))
ax.set_yticks(range(0, 21))

plt.show()
