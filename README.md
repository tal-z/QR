# Toy QR Code Generator!

This repo is a project where I am building a toy QR code generator in Python. 
The goal is to make a QR code from scratch, which re-directs to http://www.talzaken.com


### So far, I have done the following:
  - Read up on what QR codes are, where they're from, what they contain, and what each content does.
  - implemented a tiny module for converting strings into binary representation
  - implemented a function for checking whether a string is numeric, alphanumeric, latin-1, or kanji 
    - (not actually checking if kanji, just defaulting to it if none of the other 3)


### Concepts:
  - Version: this refers to the size of the grid.
  - Module: this refers to each square in the grid
  - Encoding Mode/data type: this refers to the kind of data encoded in the code. four options are numeric, alphanumeric, latin-1 text, and kanji.
  - Error correction: must understand more!!! This is what allows QR codes to be resilient to damage and mis-reads. 
    - Interestingly, it is the same tech as anti-skip on CDs. Reed-Solomon algo, which depends on finite fields (or, galios fields)
  - Finder Patterns
  - Alignment Patterns


### Exciting things:
  - I implemented a context manager for controlling whether a function prints statements or not!
    It allows me to control whether the function is verbose or not.

### Resources:
  - https://www.thonky.com/qr-code-tutorial/character-capacities
  - https://github.com/tomerfiliba/reedsolomon
  - https://github.com/mhostetter/galois
  - https://www.nayuki.io/page/qr-code-generator-library