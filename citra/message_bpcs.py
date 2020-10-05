import numpy as np
import os
from helper import encrypt_vigenere, decrypt_vigenere
import random

class MessageBPCS():
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

    mark = ['11010101', '10101010', '01010101', '10101010', '01010101', '10101010', '01010101', '10101011',]
    
    def __init__(self, path, treshold, key, encrypted, randomize):
        msg_file = open(path, "rb")
        msg_bytes = msg_file.read()
        msg_file.close()
        self.extension = os.path.splitext(path)[1].lower()[1:]
        self.m_bytes = msg_bytes
        if (encrypted):
            self.m_bytes = encrypt_vigenere(key, self.m_bytes)
        self.treshold = treshold
        self.key = key
        self.randomize = randomize
        self.encrypted = encrypted

        # get binary
        self.m_binary = self.bytes_to_binary(self.m_bytes)
        self.m_bitplane = self.binary_to_bitplane(self.m_binary)
        self.conjugation_list = self.conjugate_message()
        

    def get_message_bitplane(self):
        msg = []
        # header
        header_bitplane = self.get_header_bitplane()
        print(header_bitplane)
        # konjugation map
        conjugation_bitplane = self.get_conjugation_bitplane()
        #batas
        mark = self.binary_to_bitplane(self.mark)
        # isi pesan
        m_bitplane = self.m_bitplane
        msg = header_bitplane + conjugation_bitplane + mark + m_bitplane + mark
        print(len(header_bitplane) , len(conjugation_bitplane) , 2*len(mark) , len(m_bitplane))
        print(len(header_bitplane) + len(conjugation_bitplane) + 2*len(mark) + len(m_bitplane))
        print(len(msg))
        return msg

    def get_header_bitplane(self):
        header_m = str(int(self.randomize)) + str(int(self.encrypted)) + self.extension
        header_binary = self.bytes_to_binary(header_m.encode('latin1'))
        header_bitplane = self.binary_to_bitplane(header_binary)
        return header_bitplane

    def bytes_to_binary(self, m_bytes):
        m_binary = [format(i, '08b') for i in m_bytes]
        #padding
        while (len(m_binary) % 8 != 0):
            m_binary.append('01010101')
        return m_binary

    def binary_to_bitplane(self, m_binary):
        temp = np.array([list(i) for i in m_binary])
        m_bitplane = []
        for row in range(0, temp.shape[0] - 8 + 1, 8):
            for col in range(0, temp.shape[1] - 8 + 1, 8):
                m_bitplane.append(temp[row:row+8, col:col+8].astype(int))
        return m_bitplane
    
    def get_conjugation_bitplane(self):
        conj_map = ['0' for i in range(len(self.m_bitplane))]
        for el in self.conjugation_list:
            conj_map[el] = '1'
        
        # padding
        while(len(conj_map) % 8 != 0):
            conj_map.append('0')
        
        conj_binary = [''.join(conj_map[i:i+8]) for i in range(0, len(conj_map), 8)]
        #padding
        while(len(conj_binary) % 8 != 0):
            conj_binary.append('00000000')

        conj_bitplane = self.binary_to_bitplane(conj_binary)
        for i in range(len(conj_bitplane)):
            conj_bitplane[i] = self.conjugate(conj_bitplane[i])
        return conj_bitplane

    def conjugate_message(self):
        result = []
        for i in range(len(self.m_bitplane)):
            complexity = self.calculate_complexity(self.pbc_to_cgc(self.m_bitplane[i]))
            if (complexity < self.treshold):
                self.m_bitplane[i] = self.conjugate(self.m_bitplane[i])
                result.append(i)
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

    def conjugate(self, bitplane):
        return bitplane ^ self.konj_bitplane

    def pbc_to_cgc(self, bitplane):
        # new_bitplane = bitplane.copy()
        new_bitplane = np.array([[0 for i in range(8)] for j in range(8)])
        for i in range(8):
            new_bitplane[i][0] = bitplane[i][0]
        for i in range(8):
            for j in range(1, 8):
                new_bitplane[i][j] = bitplane[i][j-1] ^ bitplane[i][j]
        return bitplane

    

class MessageExtractorBPCS():
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

    mark = np.array([
        [1,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,1]
    ])

    byte_mark = np.array([0,1,0,1,0,1,0,1]);

    def __init__(self, msg_bitplane, key, treshold):
        self.m_bitplane = msg_bitplane
        self.key = key
        self.treshold = treshold

    def extract_message(self, path):
        print('extract message ...')
        
        #extract message
        header_bitplane = self.m_bitplane[0]
        print(header_bitplane)
        self.decode_header(header_bitplane)             #decode header
        # is random
        #extract using randomize
        if (self.randomize):
            random.seed(self.generate_seed(self.key))
            random_array = random.sample(range(64), 64)
            for i in range(1, len(self.m_bitplane)):
                self.m_bitplane[i] = self.rearrage_random_bitplane(self.m_bitplane[i], random_array)

        mark = []
        for i in range(len(self.m_bitplane)):
            if (np.array_equal(self.m_bitplane[i], self.mark)):
                mark.append(i)
        if (len(mark) != 2):
            raise Exception('Mark error.')

        conjugation_bitplane = self.m_bitplane[1:mark[0]]
        msg_bitplane = self.m_bitplane[mark[0]+1 : mark[1]]
        self.decode_conjugation(conjugation_bitplane)   #decode conjugation map
        byte_result = self.decode_message(msg_bitplane)

        file = open(path + "." + self.extension, 'wb')
        file.write(byte_result)
        file.close()

    def decode_header(self, bitplane):
        header = self.bitplane_to_byte(bitplane).decode('latin1')
        header = header.replace('U', '')
        self.randomize = bool(int(header[0]))
        self.encrypted = bool(int(header[1]))
        self.extension = header[2:]
        print(self.randomize, self.encrypted, self.extension)

    def decode_conjugation(self, bitplane):
        conj_bit = []
        temp = bitplane
        for i in range(len(temp)):
            temp[i] = self.deconjugate(temp[i])

        for bps in temp:
            for bp in bps:
                for el in bp:
                    conj_bit.append(str(el))

        self.conj_list = []
        for i in range(len(conj_bit)):
            if conj_bit[i] == '1':
                self.conj_list.append(i)
        print(self.conj_list)

    def decode_message(self, bitplane):
        msg_bitplane = bitplane

        #delete padding
        for i in range(7,-1,-1):
            if (np.array_equal(msg_bitplane[len(msg_bitplane) - 1][i], self.byte_mark)):
                msg_bitplane[len(msg_bitplane) - 1] = np.delete(msg_bitplane[len(msg_bitplane) - 1], i, axis = 0)

        #deconjugate message
        for el in self.conj_list:
            if (el < len(msg_bitplane)):
                msg_bitplane[el] = self.deconjugate(msg_bitplane[el])
        
        byte_msg = []
        for bitplane in msg_bitplane:
            byte_msg.append(self.bitplane_to_byte(bitplane))

        byte_msg = b''.join(byte_msg)
        #decrypt if encrypted
        if (self.encrypted):
            byte_msg = decrypt_vigenere(self.key, byte_msg)
        print(byte_msg.decode('latin1'))
        return byte_msg
        
    def bitplane_to_byte(self, bitplane_array):
        byte_array = []
        for plane in bitplane_array:
            temp = ''
            for cel in plane:
                temp += str(cel)
            byte = int(temp, 2)
            byte_array.append(byte)
        byte_array = bytes(byte_array)
        return byte_array

    def deconjugate(self, conj_plane):
        return conj_plane ^ self.konj_bitplane

    def rearrage_random_bitplane(self, bitplane, random_array):
        msg_bitplane = [[0 for i in range(8)] for i in range(8)]
        i = 0
        for row in range(len(msg_bitplane)):
            for col in range(len(msg_bitplane[row])):
                j = random_array[i] // 8
                k = random_array[i] % 8
                msg_bitplane[row][col] = bitplane[j,k]
                i += 1
        return np.array(msg_bitplane)

    def generate_seed(self, key):
        count = 0
        for el in key:
            count += ord(el)
        return count
    
if __name__ == "__main__":
    msg = MessageBPCS("insta.png", 0.3, 'cek', True, True)
    # print(msg.m_bitplane)
    pesan = msg.get_message_bitplane()
    # print(pesan)
    # cek1 = np.array([
    #     [1,1,0,1,0,1,0,1],
    #     [1,0,0,0,1,0,1,0],
    #     [0,1,0,1,0,0,0,1],
    #     [1,0,1,0,1,0,1,0],
    #     [0,0,0,0,0,1,0,1],
    #     [1,0,1,0,1,1,1,0],
    #     [0,1,0,1,0,1,0,1],
    #     [1,1,1,0,1,0,1,0]
    # ])
    # cek2 = msg.conjugate(cek1)
    # cek3 = msg.deconjugate(cek2)
    # print(cek1)
    # print(cek3)
    # print(cek2)