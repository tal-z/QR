
from helpers import pad_binary
from helpers import VerboseControl
from encoding_mode import get_encoding_mode

def latin1_to_padded_bytes_list(string):
    """
    :param string:
    :return list:
    """
    ba = bytearray(string, 'latin-1')
    return [pad_binary(bin(b)) for b in ba]


def latin1_to_bitstring(string):
    """
    :param string:
    :return bitstring:
    """
    binary = latin1_to_padded_bytes_list(string)
    return ''.join(binary)

def add_encoding_type_and_length(bitstring, data):
    """
    Adds 12 bits to the front of a given bitstring, representing the type of data (first 4 bits)
    and the length of the data (next 8 bits).

    :param bitstring:
    :param data:
    :return bitstring:
    """
    encoding_mode_str = ''.join(str(digit) for digit in get_encoding_mode(data))
    len_str = pad_binary(bin(len(data)))
    return encoding_mode_str + len_str + bitstring


def terminate_bitstring(bitstring, required_bits=128):
    """
    Adds a terminator to the end of a bitstring, based on a required padding length.
    :param bitstring:
    :return bitstring:
    """
    bs_len = len(bitstring)
    if bs_len > required_bits:
        raise ValueError(
            "Bitstring is too long for the number of bits required by this version and error correction level.")
    if bs_len == required_bits:
        return bitstring
    elif required_bits - bs_len < 4:
        return bitstring + '0' * (required_bits - bs_len)
    else:
        return bitstring + '0000'


def make_8_divisible_bitstring(bitstring):
    """
    Pads a terminated string with the minimum number of zeros needed to make it's length be divisible by 8
    :param bitstring:
    :return bitstring:
    """
    bs_len = len(bitstring)
    mod = bs_len % 8
    if not mod:
        return bitstring
    else:
        return bitstring + '0' * mod


def final_pad_bitstring(bitstring, required_bits=128):
    """
    Pad bitstring to required length using QR specification,
    which alternates between 8-bit representation of 236 and 17 until required bits are reached.
    :param bitstring:
    :return bitstring:
    """
    twothirtysix, seventeen = '11101100', '00010001'
    num_pads = int((required_bits - len(bitstring)) / 8)
    for i in range(num_pads):
        if not i % 2:
            bitstring += twothirtysix
        else:
            bitstring += seventeen
    return bitstring


def encode_data(data, verbose=True):
    """
    Runs pipeline to take text and convert it into bitstring necessary for encoding in a QR code.

    NOTE: This is for purely educational purposes, and is somewhat optimized for my specifically intended outcome.
            At best, this will only work with really small strings, 14 characters or less.

    :param data:
    :param verbose:
    :return bitstring:
    """
    with VerboseControl(verbose=verbose):
        print("Converting input text to bitstring using latin-1 encoding.")
        bit_string = latin1_to_bitstring(data)
        print("~~ current bitstring:", bit_string)
        print("Adding encoding type and data length to front of bitstring.")
        meta_bit_string = add_encoding_type_and_length(bit_string, data)
        print("~~ current bitstring:", meta_bit_string)
        print("Adding termination modules to bitstring based on required bit length.")
        terminated_bit_string = terminate_bitstring(meta_bit_string)
        print("~~ current bitstring:", terminated_bit_string)
        print("Padding bitstring with zeros, such that its length is divisible by eight.")
        padded_terminated_bit_string = make_8_divisible_bitstring(terminated_bit_string)
        print("~~ current bitstring:", padded_terminated_bit_string)
        print("Padding bitstring to the required bit length.")
        final_padded_terminated_bit_string = final_pad_bitstring(padded_terminated_bit_string)
        print("~~ final encoded bitstring:", final_padded_terminated_bit_string)
        return final_padded_terminated_bit_string


if __name__ == '__main__':
    print(encode_data('talzaken.com', verbose=True))
