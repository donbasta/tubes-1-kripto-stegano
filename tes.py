
import wave
import Audio
import vigenere

audio_path_tests = ['./wav/tes1.wav']
plaintext_path_tests = ['./ptext/ptext1.txt']
output_path_tests = ['./stegowav/out1.wav']
de_stego_path_tests = ['./res/res1.txt']


def stego_sound():
  # audio_path = input("Masukkan path ke audio cover: (format .wav): ")
  audio_path = audio_path_tests[0]
  # plaintext_path = input("Masukkan file yang ingin disimpan: ")
  plaintext_path = plaintext_path_tests[0]

  #convert plaintext to byte
  with open(plaintext_path, "rb") as plaintext:
    plaintext_data = plaintext.read()

  #opsi encrypt or not
  encrypted = True if input("Apakah plaintext ingin dienkripsi terlebih dahulu? (y/n): ") == 'y' else False
  if encrypted:
    plaintext_data = vigenere.encode(plaintext_data)

  scramble_position = True if input("Acak posisi plaintext pada cover? (y/n): ") == 'y' else False

  if scramble_position:
    key = int(input("Masukkan key buat random generator posisi plaintext pada cover: "))
    #TODO
    #generate random number for position, dengan seed dari key

  # output_path = input("Masukkan path buat output file: ")
  output_path = output_path_tests[0]

  #save si audio_with_plaintext balik ke folder
  Audio.hide(audio_path, plaintext_path, output_path)


def de_stego_sound():

  audio_stego_path = output_path_tests[0]
  output_path = de_stego_path_tests[0]
  num_bytes = int(input("number of bytes to recover: "))

  Audio.get(audio_stego_path, output_path, num_bytes)




if __name__ == "__main__":

  # stego_sound()

  de_stego_sound()

  




  

