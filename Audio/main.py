
import wave
# import Audio
import util
import vigenere

audio_path_tests = ['./wav/tes1.wav']
plaintext_path_tests = ['./ptext/ptext1.txt']
output_path_tests = ['./stegowav/out1.wav']
de_stego_path_tests = ['./res/res1.txt']


def testing():
  util.tes(audio_path_tests[0])


def stego_sound():

  # audio_path = input("Masukkan path ke audio cover: (format .wav): ")
  audio_path = audio_path_tests[0]
  # plaintext_path = input("Masukkan file yang ingin disimpan: ")
  plaintext_path = plaintext_path_tests[0]

  #convert plaintext to byte
  with open(plaintext_path, "r") as plaintext:
    plaintext_text = plaintext.read()

  key = input("Masukkan key buat vigenere key dan random generator posisi plaintext pada cover: ")

  encrypted = True if input("Apakah plaintext ingin dienkripsi terlebih dahulu? (y/n): ") == 'y' else False
  if encrypted:
    plaintext_text = vigenere.encode(plaintext_text, key)

  plaintext_data = bytes(plaintext_text, 'utf-8') 
  print(plaintext_data)
  #opsi encrypt or not

  scramble_seed = None

  scramble_position = True if input("Acak posisi plaintext pada cover? (y/n): ") == 'y' else False
  if scramble_position:
    scramble_seed = sum([ord(ch) - ord('A') for ch in key])
    
  print("scramble_seed = {}".format(scramble_seed))
    #TODO
    #generate random number for position, dengan seed dari key

  # output_path = input("Masukkan path buat output file: ")
  output_path = output_path_tests[0]

  #save si audio_with_plaintext balik ke folder
  util.hide(audio_path, plaintext_path, output_path, scramble_seed)


def de_stego_sound():

  # audio_stego_path = input("Masukkan path ke audio cover: (format .wav): ")
  audio_stego_path = output_path_tests[0]

  # output_path = input("Masukkan file yang ingin disimpan: ")
  output_path = de_stego_path_tests[0]

  # num_bytes = int(input("masukkan jumlah bytes yang ingin diambil: "))
  num_bytes = 10

  if encrypted:
    key = input("Masukkan kunci yang digunakan untuk enkripsi dan scramble: ")

  util.get(audio_stego_path, output_path, num_bytes)


if __name__ == "__main__":

  # testing()

  stego_sound()

  # de_stego_sound()

  




  

