# Toy QR Code Generator!

This repo is a project where I am building a toy QR code generator in Python. 
The goal is to make a QR code from scratch, which re-directs to http://www.talzaken.com


So far, I have done the following:
  - Read up on what QR codes are, where they're from, what they contain, and what each content does.
  - implemented a tiny module for converting string literals into binary strings
  - implemented a function for checking whether a string is numeric, alphanumeric, latin-1, or kanji 
    - (not actually checking if kanji, just defaulting to it if none of the other 3)



Exciting things:
  - I implemented a context manager for controlling whether a function prints statements or not!
    It allows me to control whether the function is verbose or not.