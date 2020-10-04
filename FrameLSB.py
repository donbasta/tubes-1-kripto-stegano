import base64
from PIL import Image
import math
import utils


def StringToBits(data_string: str):
    result = []
    for char in data_string:
        bits = bin(ord(char))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(bit) for bit in bits])
    return result


def BitsToString(data_bits: list):
    chars = []
    for bit in range(int(len(data_bits)/8)):
        byte = data_bits[bit*8:(bit+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


def IntToBits(data_integer: int):
    bits = bin(data_integer)[2:]
    bits = '0' * (32 - len(bits)) + bits
    return [int(bit) for bit in bits]


def BitsToInt(data_bits: list):
    res = 0
    for bit in data_bits:
        res = (res << 1) | bit
    return res


def ConstructBitsArray(data_input: str, mode: list):
    res = []
    res.extend(IntToBits(len(data_input)))
    res.extend(mode)
    res.extend(StringToBits(data_input))
    return res


class FrameLSB():
    def __init__(self, image_input: str, data_to_hide: list, target_name: str):
        self.image_input = image_input
        self.data_to_hide = data_to_hide
        self.target_name = target_name

    def hide(self):
        i = 0
        data = self.data_to_hide
        with Image.open(self.image_input) as img:
            width, height = img.size
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    for n in range(0, 3):
                        if (i < len(data)):
                            pixel[n] = pixel[n] & ~1 | int(data[i])
                            i += 1
                    img.putpixel((x, y), tuple(pixel))
            img.save(self.target_name, "PNG")

    def hide_random(self, seed):
        i = 0
        data = self.data_to_hide

        with Image.open(self.image_input) as img:
            width, height = img.size
            pixel_count = math.ceil(len(data) / 3)
            pixel_seq = utils.GenerateIntegerSequenceFromSeed(
                (width, height), pixel_count, seed)
            for index in pixel_seq:
                x = index % width
                y = math.floor(index / width)
                pixel = list(img.getpixel((x, y)))
                for n in range(0, 3):
                    if (i < len(data)):
                        pixel[n] = pixel[n] & ~1 | int(data[i])
                        i += 1
                img.putpixel((x, y), tuple(pixel))
            img.save(self.target_name, "PNG")


class FrameUnLSB():
    def __init__(self, image_input: str, target_name: str):
        self.image_input = image_input
        self.target_name = target_name

    def unhide_metadata(self, metadata_length):
        data = []
        with Image.open(self.image_input) as img:
            width, height = img.size
            byte = []
            count = 0
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    for n in range(0, 3):
                        byte.append(pixel[n] & 1)
                        count += 1
                        if count >= metadata_length:
                            break
                    if count >= metadata_length:
                        break
                if count >= metadata_length:
                    break
            data.extend(byte)
        return data

    def unhide_metadata_rand(self, metadata_length, seed):
        data = []

        with Image.open(self.image_input) as img:
            width, height = img.size
            pixel_metadata_cnt = math.ceil(metadata_length / 3)
            pixel_seq = utils.GenerateIntegerSequenceFromSeed((width, height),
                                                              pixel_metadata_cnt, seed)
            byte = []
            count = 0
            for index in pixel_seq:
                x = index % width
                y = math.floor(index / width)
                pixel = list(img.getpixel((x, y)))
                for n in range(0, 3):
                    byte.append(pixel[n] & 1)
                    count += 1
                    if count >= metadata_length:
                        break
            data.extend(byte)
        return data

    def unhide_data(self, skip_bits):
        metadata_bits = self.unhide_metadata(34)
        print(metadata_bits)
        _length = utils.BitsToInt(metadata_bits[:32])
        print("Data length on this frame: ", _length)
        mode = metadata_bits[32:34]
        data = []
        length = _length + skip_bits
        with Image.open(self.image_input) as img:
            width, height = img.size
            byte = []
            count = 0
            pos = 0
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    for n in range(0, 3):
                        # skip n-bits
                        if pos >= skip_bits:
                            byte.append(pixel[n] & 1)
                            count += 1
                        if count >= length:
                            break
                        pos += 1
                    if pos >= length:
                        break
                if pos >= length:
                    break
            data.extend(byte)
        return data

    def unhide_data_random(self, _skip_bits, seed):
        _length = utils.BitsToInt(self.unhide_metadata_rand(34, seed)[:32])
        data = []
        length = _length + _skip_bits
        print(length)
        with Image.open(self.image_input) as img:
            width, height = img.size
            pixel_seq = utils.GenerateIntegerSequenceFromSeed(
                (width, height), math.ceil(length / 3), seed)
            byte = []
            count = 0
            pos = 0
            for index in pixel_seq:
                x = index % width
                y = math.floor(index / width)
                pixel = list(img.getpixel((x, y)))
                for n in range(0, 3):
                    if pos >= _skip_bits:
                        byte.append(pixel[n] & 1)
                        count += 1
                    if count >= length:
                        break
                    pos += 1
                if pos >= length:
                    break
            data.extend(byte)
        return data
