import wave
from scipy.io import wavfile
import numpy as np
from Audio.vigenere import Vigenere
import os
import math
import random

byte_depth_to_dtype = {1: np.uint8, 2: np.uint16}

def calc_psnr(a, b):
  if a == b:
    return "Infinity"
  return 20 * math.log(b, 10) - 20 * math.log(abs(a - b))

class Audio:

  def __init__(self, path):

    extension = ['.wav']
    ext = os.path.splitext(path)[1].lower()
    if ext not in extension:
      raise Exception("Wrong file extension")
    self.audio_extension = ext

    self.path = path

    audio = wave.open(path, "r")
    
    sample_width = audio.getsampwidth()
    if sample_width != 1 and sample_width != 2:
      raise Exception("File input cannot be processed")

    audio_params = audio.getparams()
    num_channels = audio.getnchannels()
    num_frames = audio.getnframes()
    num_samples = num_frames * num_channels
    audio_frames = audio.readframes(num_frames)

    self.audio_params = audio_params
    self.num_channels = num_channels
    self.num_frames = num_frames
    self.num_samples = num_samples

    payload_dtype = byte_depth_to_dtype[sample_width]

    bit_height = len(audio_frames)
    self.payload = bit_height

    self.payload_bits = np.unpackbits(
      np.frombuffer(audio_frames, dtype=payload_dtype).view(np.uint8)
    ).reshape(bit_height, 8)

    self.array = np.array(self.payload_bits)


  def load_file_message(self, path):

    with open(path, "rb") as msg_file:
      msg_bytes = msg_file.read()

    self.msg_extension = os.path.splitext(path)[1].lower()[1:]
    if len(msg_bytes) > self.payload//8 - 1 - len(self.msg_extension) - 5:
      print("tidak muat")
      raise Exception('{} bytes file is too big'.format(len(msg_bytes)))
    self.message = msg_bytes


  def lsb(self, key=None, is_random=False, is_encrypted=False):

    if key:
      assert is_random and is_encrypted
      self.encrypt_vigenere(key)

    buff1 = ""
    buff2 = ""
    buff3 = "".join([format(ord(i), "08b") for i in "$$"])
    buff4 = "".join([format(ord(i), "08b") for i in "###"])

    if not is_random and not is_encrypted:
      buff1 = "00"
    elif is_random and is_encrypted:
      buff1 = "11"
    elif not is_random and is_encrypted:
      buff1 = "01"

    buff2 = "".join([format(ord(i), "08b") for i in self.msg_extension])
    print("buff2 : {}".format(buff2))

    self.message = "".join([format(i, "08b") for i in self.message])

    self.message = buff1 + buff2 + buff3 + self.message + buff4

    input_order = []
    if is_random:
      input_order = self.generate_random_input_order(key)
    else:
      input_order = [i for i in range(1, self.payload)]

    print("input_order encoding: {}".format(input_order[:10]))

    self.array[0][-1] = int(buff1[0])

    data_index = 1
    data_len = len(self.message)

    for pos in input_order:
      self.array[pos][-1] = int(self.message[data_index])
      data_index += 1
      if data_index >= data_len:
        break

  def decode_lsb(self, file_path, key=None):

    audio = self.array
    is_random = audio[0][-1]

    input_order = []
    if is_random == 1:
      assert key != None
      input_order = self.generate_random_input_order(key)
    else:
      input_order = [i for i in range(1, self.payload)]

    bin_message = ""
    for pos in input_order:
      bin_message += str(audio[pos][-1])

    buff1 = bin_message[:1]
    bin_message = bin_message[1:]
    is_encrypted = buff1[0]

    bytes_message = [bin_message[i:i+8] for i in range(0, len(bin_message), 8)]
    file_ext = ""

    decoded_msg = []
    temp = ""
    for byte in bytes_message:
      if file_ext == "":
        temp += chr(int(byte, 2))
        if temp[-2:] == "$$":
          file_ext = temp[:-2]
      else:
        decoded_msg.append(int(byte, 2))
        if chr(decoded_msg[-1]) == "#" and chr(decoded_msg[-2]) == "#" and chr(decoded_msg[-3]) == "#":
          decoded_msg = decoded_msg[:-3]
          break
    decoded_msg = bytes(decoded_msg)

    if is_encrypted:
      assert key != None
      decoded_msg = self.decrypt_vigenere(key, decoded_msg)

    full_file_path = file_path + "." + file_ext
    print(full_file_path)
    with open(full_file_path, "w+b") as file:
      file.write(decoded_msg)

  def encrypt_vigenere(self, key):
    cipher = Vigenere(key, key_mode=Vigenere.KeyMode.KEY_MODE_BASIC, matrix_mode=Vigenere.MatrixMode.MATRIX_MODE_FULL,
                      char_size=Vigenere.CharSize.CHAR_SIZE_EXTENDED)
    pt = cipher.encrypt(self.message.decode('latin1'))
    self.message = pt.encode('latin1')

  def decrypt_vigenere(self, key, msg):
    cipher = Vigenere(key, key_mode=Vigenere.KeyMode.KEY_MODE_BASIC, matrix_mode=Vigenere.MatrixMode.MATRIX_MODE_FULL,
                      char_size=Vigenere.CharSize.CHAR_SIZE_EXTENDED)
    ptext = cipher.decrypt(msg.decode('latin1'))
    return ptext.encode('latin1')

  def save_stego_audio(self, file_name):
    audio_frames = np.packbits(self.array).tobytes()
    with wave.open(file_name, "w") as output_file:
      output_file.setparams(self.audio_params)
      output_file.writeframes(audio_frames)

  # def save_decode_ptext(self, file_name):
  #   folder = "./out/"
  #   file_path_ext = folder + file_name + self.audio_extension
  #   with open(file_path_ext, "w+b") as output_file:
  #     output_file.write(bytes(plaintext_data))
  
  def generate_random_input_order(self, key):
    temp = [i for i in range(1, self.payload)]
    seed = sum(ord(c) for c in key)
    print("seed: {}".format(seed))
    random.seed(seed)
    random.shuffle(temp)
    return temp

  def get_amplitude(self):
    _, data = wavfile.read(self.path)
    p = np.mean(np.abs(data))
    return p

if __name__ == "__main__":

  audio_path_tests = ['./wav/tes1.wav']
  plaintext_path_tests = ['./ptext/ptext1.txt', './ptext/fsdfsf.LOL', './ptext/Resume_Farras.pdf']
  output_path_tests = ['./stegowav/out1.wav', './stegowav/out2.wav']
  de_stego_path_tests = ['./res/res1.txt', './res/res2.txt']

  while True:
    query = int(input("pilih 1. stegano, 2. de-stegano: "))

    if query == 1:

      audio_path = input("Masukkan path ke audio cover: (format .wav): ")
      audio_path = audio_path_tests[0]
      Audio = Audio(audio_path)

      plaintext_path = input("Masukkan file yang ingin dihide: ")
      plaintext_path = plaintext_path_tests[2]
      Audio.load_file_message(plaintext_path)

      output_path = input("Masukkan path buat output file: ")
      output_path = output_path_tests[0]
      Audio.lsb(is_encrypted=True, key="abc", is_random=True)
      Audio.save_stego_audio(output_path)

    elif query == 2:

      audio_stego_path = input("Masukkan path ke audio cover: (format .wav): ")
      audio_stego_path = output_path_tests[0]
      Audio = Audio(audio_stego_path)

      output_path = input("Masukkan file yang ingin disimpan: ")
      output_path = de_stego_path_tests[1]
      Audio.decode_lsb(output_path, key="abc")