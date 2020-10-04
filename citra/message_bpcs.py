import numpy as np
import os
from helper import encrypt_vigenere

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
        # self.conjugate_map = 
        

    def get_message_bitplane(self):
        msg = []

        # header
        header_msg = self.get_header_bitplane()

        # konjugation map

        # isi pesan

        # batas akhir

        return msg

    def get_header_bitplane(self):
        header_m = str(int(self.randomize)) + str(int(self.encrypted)) + self.extension
        header_binary = self.bytes_to_binary(header_m.encode('latin1'))
        header_bitplane = self.binary_to_bitplane(header_binary)
        print(header_bitplane)
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
    
    def get_conjugation_map(self, m_bitplane):
        pass

if __name__ == "__main__":
    msg = MessageBPCS("note.txt", 0.4, 'cek', True, True)
    # print(msg.m_bitplane)
    msg.get_header_bitplane()

    