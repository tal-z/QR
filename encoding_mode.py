import re
from print_context_manager import VerboseControl


numeric_re = re.compile(r'^\d*$')
alphanumeric_re = re.compile(r'^[\dA-Z $%*+\-./:]*$')
latin1_re = re.compile(r'^[\x00-\xff]*$')


def get_encoding_mode(string, verbose=True):
    with VerboseControl(verbose=verbose):
        print('Getting encoding mode')
        if numeric_re.match(string):
            print('Encoding Mode: numeric')
            return 0, 0, 0, 1
        elif alphanumeric_re.match(string):
            print('Encoding Mode: alphanumeric')
            return 0, 0, 1, 0
        elif latin1_re.match(string):
            print("Encoding Mode: latin-1")
            return 0, 1, 0, 0
        else:
            print("Encoding Mode not numeric, alphanumeric, or latin-1. Defaulting to kanji.")
            return 1, 0, 0, 0
        #return mode


if __name__ == '__main__':
    get_encoding_mode(r'http://www.talzaken.com/', verbose=True)

