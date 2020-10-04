from PIL import Image
import numpy as np
import os
import cv2
import random
from message_bpcs import MessageBPCS
'''
Algoritma BPCS
format pesan : teratur/acak , encrypted atau engga, treshold (di bitplane 1 r) ujung kiri atas
pesan ### konjugation map
'''
class CitraBPCS:
    def __init__(self, path):
        extension = ['.bmp', '.png']
        if (os.path.splitext(path)[1].lower() not in extension):
            raise Exception('Wrong file extension.')

        img = Image.open(path, 'r')
        if (img.mode == "P" or img.mode == "L"):
            self.channel = 1
        elif (img.mode == 'RGB' or img.mode == 'RGBA'):
            self.channel = 3
        else:
            raise Exception('File input cannot processed.')
        
        self.img = np.array(img)
        self.img_extension = os.path.splitext(path)[1].lower()
        self.row = self.img.shape[0]
        self.col = self.img.shape[1]

        print(self.img.shape)
        print(img.mode)

    def encode_bpcs(self, path, treshold = 0.3, randomize = False, key = None, encrypted = False):

        # msg = load massage dulu, return array of massage
        msgBPCS = MessageBPCS(path, treshold, key, encrypted, randomize)
        msg = []
        len_header = 3

        if (randomize):
            random.seed(self.generate_random_seed(key))

        msg_index = 0
        msg_len = len(msg)
        for row in range(0, self.row - 8 + 1, 8):
            for col in range(0, self.col - 8 + 1, 8):
                channels_block = cv2.split(self.img[row:row+8, col:col+8])

                channels_bitplane = [self.channel_to_bitplane(block) for block in channels_block]
                
                for i in range((self.channel)):
                    for j in range(len(channels_bitplane[i])):
                        if (msg_index < len_header):
                            channels_bitplane[i][j] = msg[msg_index]
                        else:
                            if (self.calculate_complexity(channels_bitplane[i][j]) > treshold):
                                # TO DO : convert pbt to cgc
                                if (randomize):
                                    random_array = random.sample(range(64), 64)
                                    channels_bitplane[i][j] = self.input_random_msg(channels_bitplane[i][j], msg[msg_index], random_array)
                                else:
                                    channels_bitplane[i][j] = msg[msg_index]
                                msg_index += 1

                        if msg_index >= msg_len : break
                    if msg_index >= msg_len : break

                channels_after_encode = [self.bitplane_to_channel(bitplane) for bitplane in channels_bitplane]
                # merge
                temp_block = cv2.merge(channels_after_encode)
                self.img[row:row+8, col:col+8] = temp_block

                if msg_index >= msg_len : break
            if msg_index >= msg_len : break

        # check pesan sudah ter decode semua atau belum
        if (msg_index < msg_len):
            raise Exception('Message too big.')

    def decode_bpcs():
        pass

    def input_random_msg(self, bitplane, msg, random_array):
        i = 0
        for row in msg_bitplane:
            for cell in row:
                j = random_array[i] // 8
                k = random_array % 8
                bitplane[j][k] = cell
                i += 1
        return bitplane

    def channel_to_bitplane(self, img):
        result = []
        for i in reversed(range(8)):
            result.append((img / (2 ** i)).astype(int) % 2)
        return result

    def bitplane_to_channel(self, img):
        result = (2 * (2 * (2 * (2 * (2 * (2 * (2 * img[0] + img[1])
					+ img[2]) + img[3]) + img[4])
					+ img[5]) + img[6]) + img[7])
        return result

    def calculate_complexity(self, bitplane):
        count = 0
        for i in range(8):
            for j in range(8):
                if (j != 7 and bitplane[i][j] != bitplane[i][j+1] ):
                    count += 1
                if (i != 7 and bitplane[i][j] != bitplane[i+1][j] ):
                    count += 1
        return count / 112

    def pbc_to_cgc(self, bitplane):
        pass

    def cgc_to_pbc(self, bitplane):
        pass

    def generate_random_seed(self, key):
        temp = 0
        for c in key:
            temp += ord(c)
        return temp

if __name__ == "__main__":
    citra = CitraBPCS('insta.png')
    citra.encode_bpcs('note.txt')
    konj_bitplane = np.array([
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0]
    ])
    print(citra.calculate_complexity(konj_bitplane))