import re
from print_context_manager import VerboseControl


numeric_re = re.compile(r'^\d*$')
alphanumeric_re = re.compile(r'^[\dA-Za-z $%*+\-./:]*$')
latin1_re = re.compile(r'^[\x00-\xff]*$')


def get_encoding_mode(string, verbose=True):
    with VerboseControl(verbose=verbose):
        print('Getting encoding mode')
        if numeric_re.match(string):
            print('Encoding Mode: numeric')
            return '0b0001'
        elif alphanumeric_re.match(string):
            print('Encoding Mode: alphanumeric')
            return '0b0010'
        elif latin1_re.match(string):
            print("Encoding Mode: latin-1")
            return '0b0100'
        else:
            print("Encoding Mode not numeric, alphanumeric, or latin-1. Defaulting to kanji.")
            return '0b1000'


get_encoding_mode(r'http://www.talzaken.com/', verbose=True)

