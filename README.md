# Toy QR Code Generator!

This repo is a project where I am building a toy QR code generator in Python. 
The goal is to make one single QR code from scratch, which re-directs to http://www.talzaken.com. 
It's a QR code generator that generates exactly one QR code!


### So far, I have done the following:
  - Read up on what QR codes are, where they're from, what they contain, and what each content does.
  - implemented a tiny module for converting strings into binary representation
  - implemented a function for checking whether a string is numeric, alphanumeric, latin-1, or kanji 
    - (not actually checking if kanji, just defaulting to it if none of the other 3)


### QR Code Generation Steps:
###### Step 1: Data Analysis - Determine the data type to use based on the provided text.
  - The `encoding_mode` module handles this.
###### Step 2: Data Encoding - Turning text into bits, using a method based on the text's data type
  - Choosing error correction level. Using this chart:  https://www.thonky.com/qr-code-tutorial/character-capacities
  - My desired data is 12 bytes long, so I will use an error correction level of M, which supports up to 14 bytes
  - `get_encoding_mode` returns the mode indicator, `draw_mode_indicator` renders it.
  - `draw_message_length` converts the message length to an 8-padded binary representation, and then renders it
  - Encoding of the data happens in the `latin1_to_binary` module
  - For my Version (1) and Error Correction Level (M), I will need 128 bits in the QR code.
  - because my text is only 12 characters and I am using 8-bit encoding, this adds up to 96 bits. That means I will need to terminate my bit string with four zeros.
  - after terminating, we need to make the length of the bistring divisible by 8, which we do with more padding. it becomes 104 digits long.
  - 

###### Step 3: Error Correction Coding - Using bits generated from text to generate "codewords," which help recover text if it becomes partially damaged. Reed-Solomon error correction.
###### Step 4: Structure a Final Message - This relates to the "interleaving" of data words and codewords. 
  - In the smallest of possible QR codes (like mine!), it is not necessary to "interleave". Instead, I just place the codewords after the data words.
###### Step 5: Module Placement in Matrix - This is what I've worked the most on. 
  - It includes setting individual bits of the matrix based on data, but also placement of finder marks, etc.
###### Step 6: Data Masking - Apply a transformation to the generated modules, in order to reduce patterns that make it difficult for a scanner to read the code.
  - There are 8 transformations supported by the QR specification, numbered in range(8).
  - Ideally, we should select the mask which produces the lowest "penalty score." For the purposes of this project, I will probably implement just one mask pattern.
Step 7: Format and Version information - Add information about the size of the QR code
  - Format includes error correction level and data mask
  - Version relates to the QR code's size






  1. Add Finder Patterns
  2. Add Separators (or just leave space for them)
  3. Add Alignment Patterns (not used in Version 1)
  4. Add error correction level
  5. Add the Mode (data type) Indicator
  6. Add the Character Count Indicatorv
  7. Add Timing Patterns
  8. Add Dark Module and Reserved Areas (for format and version info)
  9. Add the data (which needs to be encoded first.)


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
  - http://www.denso-wave.com/qrcode/vertable1-e.html
  - https://www.thonky.com/qr-code-tutorial/
  - https://github.com/tomerfiliba/reedsolomon
  - https://github.com/mhostetter/galois
  - https://www.nayuki.io/page/qr-code-generator-library
  - https://dev.to/maxart2501/let-s-develop-a-qr-code-generator-part-iv-placing-bits-3mn1
  - https://www.youtube.com/watch?v=142TGhaTMtI
  - https://blog.qrstuff.com/2011/12/14/qr-code-error-correction