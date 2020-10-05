import wave
import os
import lsb
import numpy as np
import math
# from oct2py import Oct2Py

byte_depth_to_dtype = {1: np.uint8, 2: np.uint16}

# def calc_psnr(a, b):
#   # if a == b:
#   #   return "No change in amplitude"
#   # return 20*math.log(b/abs(a-b), 10)

#   oc = Oct2Py()
#   script =  "function y = script(f1, f2)"
#             " [y1,fs1, nbits1,opts1]=wavread(f1);" \
#             " [y2,fs2, nbits2,opts2]=wavread(f2);" \
#             " [c1x,c1y]=size(y1);" \
#             " [c2x,c2y]=size(y1);" \
#             " R=c1x;" \
#             " C=c1y;" \
#             " err = sum((y1-y2).^2)/(R*C);" \
#             " MSE=sqrt(err);" \
#             " MAXVAL=65535;" \
#             " y = 20*log10(MAXVAL/MSE);" \
#             "end"
#   with open("./script.m","w+") as file:
#       file.write(script)

#   oc.myScript(a, b)

def tes(audio_path):
  audio = wave.open(audio_path, "r")

  audio_params = audio.getparams()
  num_channels = audio.getnchannels()
  num_frames = audio.getnframes()
  num_samples = num_frames * num_channels
  sample_width = audio.getsampwidth()
  audio_frames = audio.readframes(num_frames)

  # print(audio_frames)

  audio_dtype = byte_depth_to_dtype[sample_width]

  audio_frame_bits = np.unpackbits(
    np.frombuffer(audio_frames, dtype=audio_dtype).view(np.uint8)
  ).reshape(-1, 8 * sample_width)

  print(audio_frame_bits)
  print(audio_frame_bits.shape)

  print(sample_width)
  print("Audio params: {}".format(audio_params))
  print("Number of channels: {}".format(num_channels))
  print("Number of frames: {}".format(num_frames))
  print("Number of samples: {}".format(num_samples))
  print("Width of samples: {}".format(sample_width))

  max_size = (num_samples) // 8

  print("Max bit to hide: {}".format(max_size))

def hide(audio_path, plaintext_path, output_path, scramble_seed=None):

  audio = wave.open(audio_path, "r")

  audio_params = audio.getparams()
  num_channels = audio.getnchannels()
  num_frames = audio.getnframes()
  num_samples = num_frames * num_channels
  sample_width = audio.getsampwidth()

  print(sample_width)

  max_byte = (num_samples) // 8
  plaintext_size = os.stat(plaintext_path).st_size

  if plaintext_size > max_byte:
    raise ValueError("Ukuran file pesan melebihi payload, tidak bisa.")

  with open(plaintext_path, "rb") as plaintext:
    plaintext_data = plaintext.read()

  # print(plaintext_data)
  # print(len(plaintext_data))

  audio_frames = audio.readframes(num_frames)
  audio_frames = lsb.put_ptext(audio_frames, plaintext_data, sample_width)

  # output_file = wave.open(output_path, "w")
  # output_file.setparams(audio_params)
  # output_file.writeframes(audio_frames)
  # output_file.close()

  with wave.open(output_path, "w") as output_file:
    output_file.setparams(audio_params)
    output_file.writeframes(audio_frames)

def get(audio_path, output_path, num_bytes_to_get=10):

  audio = wave.open(audio_path, "r")

  sample_width = audio.getsampwidth()
  num_frames = audio.getnframes()
  audio_frames = audio.readframes(num_frames)

  plaintext_data = lsb.get_ptext(
    audio_frames, 8 * num_bytes_to_get, byte_depth=sample_width
  )

  with open(output_path, "w+b") as output_file:
    output_file.write(bytes(plaintext_data))