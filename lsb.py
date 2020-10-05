import numpy as np

byte_depth_to_dtype = {1: np.uint8, 2: np.uint16, 4: np.uint32, 8: np.uint64}

def put_ptext(hide, to_hide, byte_depth):

  to_hide_len = len(to_hide)

  to_hide_bits = np.zeros(shape=(to_hide_len, 8), dtype=np.uint8)
  to_hide_bits[:to_hide_len, :] = np.unpackbits(
    np.frombuffer(to_hide, dtype=np.uint8, count=to_hide_len)
  ).reshape(to_hide_len, 8)

  # print(to_hide_bits)

  bit_height = to_hide_len * 8
  to_hide_bits.resize(bit_height)

  # print(to_hide_bits)

  hide_dtype = byte_depth_to_dtype[byte_depth]

  hide_bits = np.unpackbits(
    np.frombuffer(hide, dtype=hide_dtype, count=bit_height).view(np.uint8)
  ).reshape(bit_height, 8 * byte_depth)

  print(len(hide_bits))
  print(hide_bits)

  hide_bits[:, 8 * byte_depth - 1: 8 * byte_depth] = to_hide_bits.reshape(
    bit_height, 1
  )

  ret = np.packbits(hide_bits).tobytes()
  return ret + hide[byte_depth * bit_height:]

def get_ptext(hide, num_bits, byte_depth):

  to_hide_len = num_bits
  hide_dtype = byte_depth_to_dtype[byte_depth]
  to_hide_bits = np.unpackbits(
    np.frombuffer(hide, dtype=hide_dtype, count=to_hide_len).view(np.uint8)
  ).reshape(to_hide_len, 8 * byte_depth)[:, 8 * byte_depth - 1: 8 * byte_depth]

  return np.packbits(to_hide_bits).tobytes()[: num_bits // 8]