import os, sys


class VerboseControl:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def __enter__(self):
        self._original_stdout = sys.stdout
        if not self.verbose:
            sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
