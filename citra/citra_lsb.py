import os
from PIL import Image
import numpy as np
from vigenere import Vigenere
import random
import math
from helper import decrypt_vigenere, encrypt_vigenere, pnsr

class CitraLSB:
    def __init__(self, path):
        extension = ['.bmp', '.png']
        if (os.path.splitext(path)[1].lower() not in extension):
            raise Exception('Wrong file extension.')

        img = Image.open(path, 'r')

        if (img.mode == "P" or img.mode == "L"):
            self.channel = 1
        elif (img.mode == 'RGB'):
            self.channel = 3
        elif (img.mode == 'RGBA'):
            self.channel = 3
        else:
            raise Exception('File input cannot processed.')
        
        self.ori_img = np.array(img).copy()
        self.array = np.array(img)
        self.img_extension = os.path.splitext(path)[1].lower()
        self.payload = self.channel * self.array.shape[0] * self.array.shape[1]

        print(self.payload)
        print(self.array.shape)
        print(img.mode)

    def load_file_message(self, path):
        msg_file = open(path, "rb")
        msg_bytes = msg_file.read()
        msg_file.close()
        self.msg_extension = os.path.splitext(path)[1].lower()[1:]
        if (len(msg_bytes) > self.payload//8 - 1 - len(self.msg_extension) - 5):
            raise Exception('{} bytes file is too big'.format(len(msg_bytes)))
        self.message = msg_bytes
         

    def encode_lsb(self, key='', is_random = False, is_encrypted = False):
        if (key != ''):
            self.message = encrypt_vigenere(key, self.message)

        buff1 = "" # flag random/not and encrypted/not
        buff2 = "" # flag file extension
        buff3 = ''.join([format(ord(i), '08b') for i in '$$'])
        buff4 = ''.join([format(ord(i), '08b') for i in '###']) # flag end of message

        if (not is_random and not is_encrypted):
            buff1 = '00'    # not encrypted and not random
        elif (is_random and is_encrypted):
            buff1 = '11'    # encrypted and random 
        elif (not is_random and is_encrypted):
            buff1 = '01'    # encrypted and not random
        
        buff2 = ''.join([format(ord(i), '08b') for i in self.msg_extension])
        
        self.message = (''.join([format(i, "08b") for i in self.message]))

        # merge message with buffer
        self.message = buff1 + buff2 + buff3 + self.message + buff4
        # print(self.message)
        input_order = []
        if (is_random):
            input_order = self.generate_random_input_order(key)
        else:
            input_order = [i for i in range(1, self.array.shape[0]*self.array.shape[1])]

        if (self.channel == 1):
            self.array[0][0] = int(format(self.array[0][0], '08b')[:-1] + buff1[0], 2)
        else:  
            self.array[0][0][0] = int(format(self.array[0][0][0], '08b')[:-1] + buff1[0], 2)

        data_index = 0
        data_len = len(self.message)
        #for rgb
        for el in input_order:
            i = el//self.array.shape[1]
            j = el % self.array.shape[1]
            if (self.channel == 3):
                for k in range(self.channel):
                    if (data_index < data_len):
                        self.array[i][j][k] = int(format(self.array[i][j][k], '08b')[:-1] + self.message[data_index], 2)
                        data_index += 1
            elif (self.channel == 1):
                if (data_index < data_len):
                        self.array[i][j] = int(format(self.array[i][j], '08b')[:-1] + self.message[data_index], 2)
                        data_index += 1
            if (data_index >= data_len):
                break
    
    def decode_lsb(self, file_name, key = ''):
        # TO DO : tambahin path
        image = self.array
        channel = self.channel

        if (channel == 1):
            is_random = format(image[0][0], '08b')[-1]
        else:  
            is_random = format(image[0][0][0], '08b')[-1]
        
        input_order = []
        if (is_random == '1'):
            if key == '':
                raise Exception("Need key")
            else :
                input_order = self.generate_random_input_order(key)
        else :
            input_order = input_order = [i for i in range(image.shape[0] * image.shape[1])]
        
        binary_message = ''
        for el in input_order:
            i = el//image.shape[1]
            j = el % image.shape[1]
            if (channel == 1):
                binary_message += format(image[i][j], '08b')[-1]
            else:
                for k in range(channel):
                    binary_message += format(image[i][j][k], '08b')[-1]
        print(binary_message[0:100])
        buff1 = binary_message[:1]
        binary_message = binary_message[1:]
        is_encrypted = buff1[0]

        bytes_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        file_extension = ''

        decoded_msg = []
        temp = ''
        for byte in bytes_message:
            if file_extension == '':
                # print("cekcek")
                temp += chr(int(byte, 2))
                if temp[-2:] == "$$":
                    file_extension = temp[:-2]
            else :
                decoded_msg.append(int(byte, 2))
                if chr(decoded_msg[-1]) == "#" and chr(decoded_msg[-2]) == "#" and chr(decoded_msg[-3]) == "#":
                    decoded_msg = decoded_msg[:-3]
                    break
        decoded_msg = bytes(decoded_msg)

        if is_encrypted == '1':
            print("pesan di enkripsiii")
            if key == '':
                raise Exception("Need a key")
            else :
                decoded_msg = decrypt_vigenere(key, decoded_msg)

        print('='*50)
        # print(file_extension)
        # print(bytes(decoded_msg))
        file = open(file_name + "."+file_extension, 'wb')
        file.write(decoded_msg)
        file.close()

    def save_stego_image(self, file_name):
        im = Image.fromarray(self.array)
        im.save(file_name + self.img_extension)

    def generate_random_input_order(self, key):
        temp = [i for i in range(1, self.array.shape[0]*self.array.shape[1])]
        seed = 0
        for c in key:
            seed += ord(c)
        random.seed(seed)
        random.shuffle(temp)
        return temp

    def get_pnsr(self):
        print(pnsr(self.array, self.ori_img))
        return pnsr(self.array, self.ori_img)

if __name__ == "__main__":
    # while(True):
    #     print("Pilih : 1. sisipkan, 2. decode")
    #     inp = int(input("masukkan pilihan"))
    #     if inp == 1:
    #         input_img = str(input("Masukkan path gambar : "))
    #         input_msg = str(input("masukkan path pesan : "))
    #         citra = CitraLSB(input_img)
    #         citra.load_file_message(input_msg)
    #         citra.encode_lsb()
    #         file_name = str(input("Masukkan nama gambar hasil stego untuk disimpan :"))
    #         citra.save_stego_image(file_name)
    #         print("PNSR : " , pnsr(citra.array, citra.ori_img))
    #     elif inp == 2 :
    #         input_img = str(input("Masukkan path gambar : "))
    #         file_name = str(input("Masukkan nama gambar pesan untuk disimpan :"))
    #         citra = CitraLSB(input_img)
    #         citra.decode_lsb(file_name)
    
    citra = CitraLSB('hasil/stego.png')
    citra.decode_lsb('hasil/note')
