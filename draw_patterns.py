
import numpy as np

from helpers import pad_binary, VerboseControl
from encoding_mode import get_encoding_mode
from latin1_to_binary import encode_data
from error_correction import generate_code_words


def draw_finder_patterns(grid, verbose=True):
    """fills in corners of grid with easily-recognized square QR pattern"""
    with VerboseControl(verbose=verbose):
        print("Drawing finder patterns")
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


def draw_timing_patterns(grid, verbose=True):
    """
    Fills in relevant area with evenly-spaced pattern of alternating black and white modules,
    used to tell the scanner the size of modules and the version of QR code being interpreted.
    This is the Version 1 timing pattern.
    """
    with VerboseControl(verbose=verbose):
        print("Drawing timing patterns")
        for i, row in enumerate(grid):
            for j, square in enumerate(row):
                if (i == 6) and (7 < j < 13) and (j % 2 == 0):
                    grid[i, j] = 1
                if (j == 6) and (7 < i < 13) and (i % 2 == 0):
                    grid[i, j] = 1


def draw_dark_module(grid, verbose=True):
    with VerboseControl(verbose=verbose):
        print("Drawing dark module")
        grid[13, 8] = 1


def draw_error_correction_level(grid, level='M', verbose=True):
    """
    Super informative blog post: https://blog.qrstuff.com/2011/12/14/qr-code-error-correction
    """
    with VerboseControl(verbose=verbose):
        print("Drawing error correction level")
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


def draw_mask_pattern(grid, pattern_num=0, verbose=True):
    """
    Mask Pattern explainer: https://www.thonky.com/qr-code-tutorial/mask-patterns

    Mask Pattern 0: (row + column) % 2 == 0
    if the coordinates for a given bit match the above formula, switch the value of the bit.
    """
    with VerboseControl(verbose=verbose):
        print("Drawing mask pattern in format string")
        if pattern_num > 0:
            raise ValueError(f"Currently only mask pattern 0 is supported. You enetered '{pattern_num}'.")
        grid[8, 2], grid[8, 3], grid[8, 4] = 1, 0, 0
        grid[18, 8], grid[17, 8], grid[16, 8] = 1, 0, 0


def draw_mode_indicator(grid, data, verbose=True):
    """https://merricx.github.io/qrazybox/help/getting-started/about-qr-code.html"""
    with VerboseControl(verbose=verbose):
        print("Drawing mode indicator modules")
        grid[20, 20], grid[20, 19], grid[19, 20], grid[19, 19] = get_encoding_mode(data)


def draw_message_length(grid, data, verbose=True):
    with VerboseControl(verbose=verbose):
        print("Drawing message length")
        padded_binary_string = pad_binary(bin(len(data)))
        binary_values = (int(digit) for digit in padded_binary_string)
        grid[18, 20], grid[18, 19], \
        grid[17, 20], grid[17, 19], \
        grid[16, 20], grid[16, 19], \
        grid[15, 20], grid[15, 19] = binary_values



def draw_data(grid, data, verbose=True):
    """
    update matrix with data from encoded bitstring.
    This includes encoding type and data length,
    but not the error correction codewords.

    :param grid:
    :param data:
    :return:
    """
    Z = [
        (0, 0), (0, 1),
        (1, 0), (1, 1)
    ]

    STARTS = [
        (20, 20, True),    (18, 20, True),   
        (16, 20, True),    (14, 20, True),
        (12, 20, True),    (10, 20, True),
        (9, 18, False),     (11, 18, False),
        (13, 18, False),    (15, 18, False),
        (17, 18, False),    (19, 18, False),
        (20, 16, True),    (18, 16, True),
        (16, 16, True),    (14, 16, True),
        (12, 16, True),    (10, 16, True),
        (9, 14, False),     (11, 14, False),
        (13, 14, False),    (15, 14, False),
        (17, 14, False),    (19, 14, False),
        (20, 12, True),    (18, 12, True),
        (16, 12, True),    (14, 12, True),
        (12, 12, True),    (10, 12, True),
        (8, 12, True),      (5, 12, True), 
    ]

    with VerboseControl(verbose=verbose):
        print("Drawing data, including mode indicator and message length")
        bitstring = encode_data(data)

        for ind, (i, j, up) in enumerate(STARTS): # up is a bool
            # zigzag is 4 bit coordinates in the qr code
            zigzag = [(i-x, j-y) for x,y in Z] if up else [(i+x, j-y) for x,y in Z]
            # for each zigzag coordinate, change the grid cell according to the bit
            for bit, coor in zip(bitstring[ind*4:ind*4+4], zigzag):
                grid[coor] = bit


def draw_code_words(grid, data, verbose=True):
    with VerboseControl(verbose=verbose):
        print("Drawing code words")
        coordinates_dict = {
            0: [(3, 12), (3, 11), (2, 12), (2, 11), (1, 12), (1, 11), (0, 12), (0, 11)],
            1: [(0, 10), (0, 9), (1, 10), (1, 9), (2, 10), (2, 9), (3, 10), (3, 9)],
            2: [(4, 10), (4, 9), (5, 10), (5, 9), (7, 10), (7, 9), (8, 10), (8, 9)],
            3: [(9, 10), (9, 9), (10, 10), (10, 9), (11, 10), (11, 9), (12, 10), (12, 9)],
            4: [(13, 10), (13, 9), (14, 10), (14, 9), (15, 10), (15, 9), (16, 10), (16, 9)],
            5: [(17, 10), (17, 9), (18, 10), (18, 9), (19, 10), (19, 9), (20, 10), (20, 9)],
            6: [(12, 8), (12, 7), (11, 8), (11, 7), (10, 8), (10, 7), (9, 8), (9, 7)],
            7: [(9, 5), (9, 4), (10, 5), (10, 4), (11, 5), (11, 4), (12, 5), (12, 4)],
            8: [(12, 3), (12, 2), (11, 3), (11, 2), (10, 3), (10, 2), (9, 3), (9, 2)],
            9: [(9, 1), (9, 0), (10, 1), (10, 0), (11, 1), (11, 0), (12, 1), (12, 0)],
        }
        code_words = generate_code_words(data)
        for idx in range(10):
            coordinates = coordinates_dict[idx]
            bits = code_words[idx]
            for bit, coord in zip(bits, coordinates):
                grid[coord] = bit


def apply_mask(grid, mask_pattern=1, verbose=True):
    """
    Mask Pattern explainer: https://www.thonky.com/qr-code-tutorial/mask-patterns

    :param grid:
    :param mask_pattern:
    :return:
    """
    with VerboseControl(verbose=verbose):
        print(f"Applying mask pattern {mask_pattern}")
        function_pattern_coords = {
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 20),
            (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20),
            (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (3, 20),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20),
            (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 13), (7, 14), (7, 15), (7, 16), (7, 17), (7, 18), (7, 19), (7, 20),
            (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 13), (8, 14), (8, 15), (8, 16), (8, 17), (8, 18), (8, 19), (8, 20),
            (12, 0), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8),
            (13, 0), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8),
            (14, 0), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8),
            (15, 0), (15, 1), (15, 2), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7), (15, 8),
            (16, 0), (16, 1), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8),
            (17, 0), (17, 1), (17, 2), (17, 3), (17, 4), (17, 5), (17, 6), (17, 7), (17, 8),
            (18, 0), (18, 1), (18, 2), (18, 3), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8),
            (19, 0), (19, 1), (19, 2), (19, 3), (19, 4), (19, 5), (19, 6), (19, 7), (19, 8),
            (20, 0), (20, 1), (20, 2), (20, 3), (20, 4), (20, 5), (20, 6), (20, 7), (20, 8),
            (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12)
        }
        if mask_pattern != 1:
            raise ValueError(f"Currently only mask pattern 1 is supported. You entered '{mask_pattern}'.")
        for coord, val in np.ndenumerate(grid):
            if coord in function_pattern_coords:
                pass
            else:
                if coord[0] % 2 == 0:
                    grid[coord] = not grid[coord]


def draw_format_strings(grid, ecl='M', mask_pattern=1, verbose=True):
    """
    Format String explainer: https://www.thonky.com/qr-code-tutorial/format-version-information

    :param grid:
    :param ecl:
    :param mask_pattern:
    :return:
    """
    with VerboseControl(verbose=verbose):
        print("Drawing format string based on error correction level and mask pattern")
        if mask_pattern != 1 or ecl.upper() != 'M':
            raise ValueError(f"Currently only mask pattern 1 with error correction level 'M' is supported. You entered mask pattern '{mask_pattern}' with error correction level '{ecl}'.")
        format_string = '101000100100101'
        format_bits = {
            0: [(8, 0), (20, 8)],
            1: [(8, 1), (19, 8)],
            2: [(8, 2), (18, 8)],
            3: [(8, 3), (17, 8)],
            4: [(8, 4), (16, 8)],
            5: [(8, 5), (15, 8)],
            6: [(8, 7), (14, 8)],
            7: [(8, 8), (8, 13)],
            8: [(7, 8), (8, 14)],
            9: [(5, 8), (8, 15)],
            10: [(4, 8), (8, 16)],
            11: [(3, 8), (8, 17)],
            12: [(2, 8), (8, 18)],
            13: [(1, 8), (8, 19)],
            14: [(0, 8), (8, 20)],
        }

        for idx in range(15):
            coord_a, coord_b = format_bits[idx]
            grid[coord_a], grid[coord_b] = format_string[idx], format_string[idx]


def brute_force_post_masked_codewords(grid, verbose=True):
    with VerboseControl(verbose=verbose):
        print("Brute-forcing the correct code words into place")
        coordinates_dict = {
            0: [(3, 12), (3, 11), (2, 12), (2, 11), (1, 12), (1, 11), (0, 12), (0, 11)],
            1: [(0, 10), (0, 9), (1, 10), (1, 9), (2, 10), (2, 9), (3, 10), (3, 9)],
            2: [(4, 10), (4, 9), (5, 10), (5, 9), (7, 10), (7, 9), (8, 10), (8, 9)],
            3: [(9, 10), (9, 9), (10, 10), (10, 9), (11, 10), (11, 9), (12, 10), (12, 9)],
            4: [(13, 10), (13, 9), (14, 10), (14, 9), (15, 10), (15, 9), (16, 10), (16, 9)],
            5: [(17, 10), (17, 9), (18, 10), (18, 9), (19, 10), (19, 9), (20, 10), (20, 9)],
            6: [(12, 8), (12, 7), (11, 8), (11, 7), (10, 8), (10, 7), (9, 8), (9, 7)],
            7: [(9, 5), (9, 4), (10, 5), (10, 4), (11, 5), (11, 4), (12, 5), (12, 4)],
            8: [(12, 3), (12, 2), (11, 3), (11, 2), (10, 3), (10, 2), (9, 3), (9, 2)],
            9: [(9, 1), (9, 0), (10, 1), (10, 0), (11, 1), (11, 0), (12, 1), (12, 0)],
        }
        spaced_bitstring = '11000001 00101111 10000100 00110011 10010001 10110100 11111111 10101110 00001110 10000101'
        code_words = spaced_bitstring.split()
        for idx in range(10):
            coordinates = coordinates_dict[idx]
            bits = code_words[idx]
            for bit, coord in zip(bits, coordinates):
                grid[coord] = bit
