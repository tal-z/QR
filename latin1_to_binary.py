
def pad_binary(string):
    pad = 8 - (len(string) - 2)
    return '0' * pad + string[2:]


def latin1_to_bitstring(string):
    ba = bytearray(string, 'latin-1')
    binary = [pad_binary(bin(b)) for b in ba]
    return ''.join(binary)


def terminate_bitstring(bitstring, required_bits=128):
    """adds a terminator to the end of a bitstring, based on a required padding length"""
    bs_len = len(bitstring)
    if bs_len > required_bits:
        raise ValueError("Bitstring is too long for the number of bits required by this version and error correction level.")
    if bs_len == required_bits:
        return bitstring
    elif required_bits - bs_len < 4:
        return bitstring + '0' * (required_bits - bs_len)
    else:
        return bitstring + '0000'


def make_8_divisible_bitstring(bitstring):
    bs_len = len(bitstring)
    mod = bs_len % 8
    if not mod:
        return bitstring
    else:
        return bitstring + '0' * mod



if __name__ == '__main__':
    s = 'talzaken.com'
    bs = latin1_to_bitstring(s)
    print(bs)
    print(len(bs))

    tbs = terminate_bitstring(bs)
    print(len(tbs))
    ptbs = make_8_divisible_bitstring(tbs)
    print(len(ptbs))


