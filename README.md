# Toy QR Code Generator!

I built a toy QR code generator in Python. 
The goal was to make one single QR code from scratch, which re-directs to talzaken.com. 
It's a QR code generator that generates exactly one QR code!

![talzaken.com](https://raw.githubusercontent.com/tal-z/QR/master/QR.png)

### Why build a toy QR code generator?
My purpose in building a toy QR code generator was to understand the structure of QR codes, 
the steps needed to build them, and the basic concept of error correcting codes. Mission accomplished!


#### QR Code Structure:
  1. Finder Patterns: these are the three easily-recognizable squares in the top left and right, and bottom left corners of the QR code
  2. Timing Patterns: this tells the QR code scanner the block size to be scanned
  3. Alignment patterns: not used in V1 QR codes
  4. Format pattern: tells the QR decoder the level of error correction and the mask pattern
  5. Encoding mode: tells the QR scanner the type of data being encoded
  6. Message length: tells the QR scanner how much data there is to be decoded
  7. Data: this is the data that's encoded.
  8. Dark Module: This is a module that is always dark. It's mostly unused.
  9. Reserved spaces: whitespace that lets the QR code recognize the location of patterns.


#### QR Code Generation Steps:
###### Step 1: Data Analysis - Determine the data type to use based on the provided text.
  - The `encoding_mode` module handles this.
###### Step 2: Data Encoding - Turning text into bits, using a method based on the text's data type
  - Choosing error correction level. Using this chart:  https://www.thonky.com/qr-code-tutorial/character-capacities
  - My desired data is 12 bytes long, so I will use an error correction level of M, which supports up to 14 bytes
  - `get_encoding_mode` returns the mode indicator, which is used in `latin1_to_binary` when encoding the data code words.
  - Encoding of the data happens in the `latin1_to_binary` module.
    - This includes necessary padding each step of the way.
  - For my Version (1) and Error Correction Level (M), I will need 128 bits in the QR code.
  - Because my text is only 12 characters and I am using 8-bit encoding, this adds up to 96 bits. Including the padded message length and mode indicator bits, this comes to a total of 108 bits. That means I will need to terminate my bit string with four zeros.
  - After terminating, we need to make the length of the bistring divisible by 8, which we do with more padding. it becomes 112 digits long.
  - Finally, we need to pad until we reach 128 bits, but we need to do so according the the QR standard, which is to pad with alternating binary representation of 236 and 17 respectively, until the correct bit length has been reached.

###### Step 3: Error Correction Coding - Using bits generated from text to generate "codewords," which help recover text if it becomes partially damaged. Reed-Solomon error correction.
  - We need to generate error correction codewords, and the number of codewords is based on the version and error correction level of our QR code.
  - I need 10 code words. 
###### Step 4: Structure a Final Message - This relates to the "interleaving" of data words and codewords. 
  - In the smallest of possible QR codes (like mine!), it is not necessary to "interleave". Instead, I just place the codewords after the data words.
###### Step 5: Module Placement in Matrix - This is what I've worked the most on. 
  - It includes setting individual bits of the matrix based on data, but also placement of finder marks, etc.
###### Step 6: Data Masking - Apply a transformation to the generated modules, in order to reduce patterns that make it difficult for a scanner to read the code.
  - There are 8 transformations supported by the QR specification, numbered in range(8).
  - Ideally, we should select the mask which produces the lowest "penalty score." For the purposes of this project, I have implemented just one mask pattern (number 1).
###### Step 7: Format and Version information - Add information about the size of the QR code
  - Format includes error correction level and data mask
  - Version relates to the QR code's size
  - The format string also contains error correction codewords. However, since there are only 8 masks and four error correction levels, there are only 32 possible format strings. This saves us the heavy lifting of needing to generate code words again.


### Exciting things not related to QR codes:
  - I implemented a context manager! It controls whether a function prints statements or not. 
    This is a nice, pythonic way to implement flow control for verbosity.


### Resources:
  - http://www.denso-wave.com/qrcode/vertable1-e.html
  - https://www.thonky.com/qr-code-tutorial/
  - https://github.com/tomerfiliba/reedsolomon
  - https://github.com/mhostetter/galois
  - https://www.nayuki.io/page/qr-code-generator-library
  - https://dev.to/maxart2501/let-s-develop-a-qr-code-generator-part-iv-placing-bits-3mn1
  - https://www.youtube.com/watch?v=142TGhaTMtI
  - https://blog.qrstuff.com/2011/12/14/qr-code-error-correction
