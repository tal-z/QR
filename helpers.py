
def pad_binary(string):
    pad = 8 - (len(string) - 2)
    return '0' * pad + string[2:]

def bitstring_to_bytes(bitstring):
    return [bitstring[idx:idx+8] for idx in range(0, len(bitstring), 8)]


if __name__ == '__main__':
    print(bitstring_to_bytes('100011101010111100000101'))