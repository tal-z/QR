'''## Early Attempts
"""
const LOG = new Uint8Array(256);
const EXP = new Uint8Array(256);
for (let exponent = 1, value = 1; exponent < 256; exponent++) {
  value = value > 127 ? ((value << 1) ^ 285) : value << 1;
  LOG[value] = exponent % 255;
  EXP[exponent % 255] = value;
}
"""

log = {}
exp = {}
value = 1
for exponent in range(1, 256):
    value = ((value << 1) ^ 285) if value > 127 else value << 1
    log[value] = exponent % 255
    exp[log[value]] = value


"""
function mul(a, b) {
  return a && b ? EXP[(LOG[a] + LOG[b]) % 255] : 0;
}
function div(a, b) {
  return EXP[(LOG[a] + LOG[b] * 254) % 255];
}
"""


def mul(a, b):
    return exp[(log[a] + log[b]) % 255] if (a and b) else 0


def div(a, b):
    return exp[((log[a] + log[b] * 254) % 255)]

print(mul(16, 32))

'''
from reedsolo import RSCodec
from helpers import pad_binary, VerboseControl



def generate_code_words(string, verbose=True):
    with VerboseControl(verbose=verbose):
        print("Encoding string as ascii.")
        b_string = string.encode('ascii')
        print("~~ascii string:", b_string)
        print("Initializing Reed-Solomon Codec for calculating error correction codes.")
        rsc = RSCodec(10) # 10 is the amount of space left in the QR code based on the Version and chosen Error Correction Level.
        print('Encoding the binary string.')
        code = rsc.encode(b_string)
        print('~~encoded data with error correction:', *code)
        print('Converting code words to binary.')
        code_words = code[-10:]
        binary_code_words = [pad_binary(bin(num)) for num in code_words]
        print('~~binary code words:', binary_code_words)
        print('Returning code words as binary.')
        return binary_code_words

if __name__ == '__main__':
    generate_code_words('talzaken.com')





















