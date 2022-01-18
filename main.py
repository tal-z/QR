
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

from draw_patterns import (draw_finder_patterns, draw_timing_patterns,
                           draw_dark_module, draw_data,
                           draw_code_words, draw_format_strings,
                           apply_mask, brute_force_post_masked_codewords)
from helpers import VerboseControl


v1_base_grid = np.zeros((21, 21))

def main(string, verbose=True):
    with VerboseControl(verbose=verbose):
        # Update the grid with QR code data
        draw_finder_patterns(v1_base_grid)
        draw_timing_patterns(v1_base_grid)
        draw_dark_module(v1_base_grid)
        draw_data(v1_base_grid, string)
        # draw_code_words(v1_base_grid, 'talzaken.com')
        draw_format_strings(v1_base_grid)
        apply_mask(v1_base_grid)
        brute_force_post_masked_codewords(v1_base_grid)

        # Plot and show the QR Code
        fig, ax = plt.subplots()
        cmap = colors.ListedColormap(['white', 'black'])
        plt.imshow(v1_base_grid, cmap=cmap)
        plt.axis('off')

        plt.show()


if __name__ == '__main__':
   main('talzaken.com', verbose=True)
