
import wave
import os
import lsb

def hide(audio_path, plaintext_path, output_path):

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
    raise ValueError("Not enough bytes in the audio to hide the file.")

  with open(plaintext_path, "rb") as plaintext:
    plaintext_data = plaintext.read()

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