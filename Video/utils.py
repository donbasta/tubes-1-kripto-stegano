def StringToBits(data_string: str):
    result = []
    for char in data_string:
        bits = bin(ord(char))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(bit) for bit in bits])
    return result


def RawStringToBits(data_string: str):
    result = []
    for char in data_string:
        bits = bin(char)[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(bit) for bit in bits])
    return result


def BitsToString(data_bits: list):
    chars = []
    for bit in range(int(len(data_bits)/8)):
        byte = data_bits[bit*8:(bit+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def BitsToRawString(data_bits: list):
    chars = []
    for bit in range(int(len(data_bits)/8)):
        byte = data_bits[bit*8:(bit+1)*8]
        chars.append(int(''.join([str(bit) for bit in byte]), 2))
    return bytes(chars)


def IntToBits(data_integer: int):
    bits = bin(data_integer)[2:]
    bits = '0' * (32 - len(bits)) + bits
    return [int(bit) for bit in bits]


def BitsToInt(data_bits: list):
    res = 0
    for bit in data_bits:
        res = (res << 1) | bit
    return res


def GenerateIntegerSequenceFromSeed(dimension: tuple, length: int, seed: int, skip=0):
    import random
    random.seed(seed)
    pixel_cnt = dimension[0] * dimension[1]
    res = random.sample(range(skip, pixel_cnt), length)
    return res


def ConstructVideoMetadata(title: str, ext: str):
    if len(title) >= 33:
        print("Video title length max is 31 char")
        return []
    if len(ext) >= 6:
        print("Video ext length max is 5 char")
        return []
    title_bits = StringToBits(title)
    ext_bits = StringToBits(ext)
    if len(title_bits) < 32 * 8:
        # padding
        for i in range(len(title), 32):
            title_bits.extend([0, 0, 0, 0, 0, 0, 0, 0])
    if len(ext_bits) < 5 * 8:
        # padding
        for i in range(len(ext), 5):
            ext_bits.extend([0, 0, 0, 0, 0, 0, 0, 0])
    data = []
    data.extend(title_bits)
    data.extend(ext_bits)
    print(len(title_bits))
    print(len(ext_bits))
    print(BitsToString(title_bits))
    return data


# metadata_bitfield = ConstructVideoMetadata(
#     "aaaabbbbccccddddeeeeffffgggghhhh", "ts")
# print(len(metadata_bitfield))
# print(ConstructModeMetadata([1, 1], 69420))
# print(ConstructModeMetadata([0, 0], 0))
# print(len(ConstructModeMetadata([0, 0], 1023)))
