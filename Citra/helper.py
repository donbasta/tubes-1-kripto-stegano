from Citra.vigenere import Vigenere
import math
import numpy as np

def pnsr(image1, image2):
    rms = math.sqrt(np.sum((image1.astype('float') - image2.astype('float')) ** 2) / (image1.shape[1] * image1.shape[0]))
    return 20 * math.log10(256 / rms)

def encrypt_vigenere(key, msg):
    cipher = Vigenere(key, key_mode=Vigenere.KeyMode.KEY_MODE_BASIC, matrix_mode=Vigenere.MatrixMode.MATRIX_MODE_FULL,
                    char_size=Vigenere.CharSize.CHAR_SIZE_EXTENDED)
    pt = cipher.encrypt(msg.decode('latin1'))
    return pt.encode('latin1')

def decrypt_vigenere(key, msg):
    cipher = Vigenere(key, key_mode=Vigenere.KeyMode.KEY_MODE_BASIC, matrix_mode=Vigenere.MatrixMode.MATRIX_MODE_FULL,
                    char_size=Vigenere.CharSize.CHAR_SIZE_EXTENDED)
    pt = cipher.decrypt(msg.decode('latin1'))
    return pt.encode('latin1')