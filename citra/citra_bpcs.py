from PIL import Image
import numpy as np
import os
import cv2
import random
from message_bpcs import MessageBPCS, MessageExtractorBPCS
import time
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
        self.img_ori = np.array(img)
        self.img = np.array(img)
        self.img_extension = os.path.splitext(path)[1].lower()
        self.row = self.img.shape[0]
        self.col = self.img.shape[1]

        print(self.img.shape)
        print(img.mode)

    def encode_bpcs(self, path, treshold = 0.3, randomize = False, key = None, encrypted = False):

        # msg = load massage dulu, return array of massage
        msgBPCS = MessageBPCS(path, treshold, key, encrypted, randomize)
        msg = msgBPCS.get_message_bitplane()

        random_array = []
        if (randomize):
            random.seed(self.generate_random_seed(key))
            random_array = random.sample(range(64), 64)
        msg_index = 0
        msg_len = len(msg)
        for row in range(0, self.row - 8 + 1, 8):
            for col in range(0, self.col - 8 + 1, 8):
                channels_block = cv2.split(self.img[row:row+8, col:col+8])

                channels_bitplane = [self.channel_to_bitplane(block) for block in channels_block]
                
                for i in range((self.channel)):
                    for j in range(len(channels_bitplane[i])):
                        if (self.calculate_complexity(self.pbc_to_cgc( channels_bitplane[i][j] )) > treshold):
                            # TO DO : convert pbt to cgc
                            if (randomize and msg_index != 0):
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

    def decode_bpcs(self, path, treshold = 0.3, key = None):
        msg_bitplane = []
        for row in range(0, self.row - 8 + 1, 8):
            for col in range(0, self.row - 8 + 1, 8):
                channels_block = cv2.split(self.img[row:row+8, col:col+8])
                channels_bitplane = [self.channel_to_bitplane(block) for block in channels_block]

                for i in range(self.channel):
                    for bitplane in channels_bitplane[i]:
                        if (self.calculate_complexity(self.pbc_to_cgc(bitplane)) > treshold):
                            msg_bitplane.append(bitplane)
        
        msgBPCS = MessageExtractorBPCS(msg_bitplane, key, treshold)
        msgBPCS.extract_message(path)

        


    def input_random_msg(self, bitplane, msg, random_array):
        i = 0
        for row in msg:
            for cell in row:
                j = random_array[i] // 8
                k = random_array[i] % 8
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

    def generate_random_seed(self, key):
        temp = 0
        for c in key:
            temp += ord(c)
        return temp

    def save_stego_image(self, file_name):
        im = Image.fromarray(self.img)
        im.save(file_name + self.img_extension)

    def pbc_to_cgc(self, bitplane):
        new_bitplane = np.array([[0 for i in range(8)] for j in range(8)])
        for i in range(8):
            new_bitplane[i][0] = bitplane[i][0]
        for i in range(8):
            for j in range(1, 8):
                new_bitplane[i][j] = bitplane[i][j-1] ^ bitplane[i][j]
        return bitplane

if __name__ == "__main__":
    s = time.time()
    citra = CitraBPCS('gambar/raw.png')
    citra.encode_bpcs('pesan/msg.txt', key = 'lala', encrypted=True, randomize=True, treshold=0.3)
    citra.save_stego_image('hasil/bpcs')

    c_decode = CitraBPCS('hasil/bpcs.bmp')
    c_decode.decode_bpcs(key='lala', treshold=0.3)
    e = time.time()
    print(e - s)

    # konj_bitplane = np.array([
    #     [1,1,0,1,0,1,0,1],
    #     [1,0,1,0,1,0,1,0],
    #     [1,1,0,1,0,1,0,1],
    #     [1,0,1,0,1,0,1,0],
    #     [0,1,0,1,0,1,0,1],
    #     [0,0,1,0,1,0,1,0],
    #     [0,1,0,1,0,1,0,1],
    #     [0,1,0,1,0,1,0,1]
    # ])
    # print(konj_bitplane[0][0])
    # cek2 = citra.pbc_to_cgc(konj_bitplane)
    # print(cek2)
    # print(konj_bitplane)
