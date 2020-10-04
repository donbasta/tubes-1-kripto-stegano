import numpy as np


class Vigenere():
    def __init__(self):
        self.key = ""
        self.full = False
        self.auto = False
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.extended = False
        self.make_matrix()
        self.full_matrix = self.matrix
        for i in range(26):
            self.full_matrix[i][1:] = np.random.permutation(self.matrix[i][1:])

    def set_full(self, _full):
        self.full = _full
        if self.full:
            self.matrix = self.full_matrix
        else:
            self.make_matrix()

    def set_auto(self, _auto):
        self.auto = _auto

    def set_extended(self, _extended):
        self.extended = _extended
        if (_extended):
            self.alphabet = [c for c in (chr(i) for i in range(0, 256))]
        else:
            self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.make_matrix()

    def input_key(self, key):
        self.key = key

    def shuffle_matrix(self):
        self.make_matrix()

    def make_matrix(self):
        np_alphabet = np.array(list(self.alphabet))
        if self.extended:
            cnt = 256
        else:
            cnt = 26
        self.matrix = np.empty(shape=(0, cnt))
        for i in range(cnt):
            mod_alphabet = np.roll(np_alphabet, -1*i)
            self.matrix = np.append(self.matrix, [mod_alphabet], axis=0)

    def expand_key(self, text: str):
        # expand key to encrypt plain text
        text_len = len(text)
        expanded_key = self.key
        expanded_key_len = len(self.key)
        while expanded_key_len < text_len:
            if self.auto:
                expanded_key = expanded_key + text
            else:
                expanded_key = expanded_key + self.key
            expanded_key_len = len(expanded_key)
        return expanded_key

    def encrypt(self, text: str):
        print("Encrypting...")
        if not self.extended:
            text = text.upper()
            self.key = self.key.upper()
        expanded_key = self.expand_key(text)
        # encrypt
        print(text)
        key_pos = 0
        null_count = 0
        ciphertext = []
        print(self.matrix)
        for letter in text:
            if letter in self.alphabet:
                search_text = np.where(self.matrix[0] == letter)
                search_key = np.where(
                    self.matrix[:, 0] == expanded_key[key_pos])
                key_pos += 1
                idx_text = search_text[0][0]
                idx_key = search_key[0][0]
                if self.matrix[idx_key][idx_text] == '':
                    null_count += 1
                    ciphertext.append(0)
                else:
                    ciphertext.append(ord(self.matrix[idx_key][idx_text]))
        # print("Final text is: {}".format(ciphertext))
        print("Keypos: ", key_pos)
        print("Encrypted length: ", len(ciphertext))
        print("Null count: ", null_count, "null char:", "\x00", "there")
        return ciphertext

    def decrypt(self, text: str):
        print("Decrypting...")
        plaintext = ""
        if self.auto:
            plaintext = self.decrypt_auto_key(text)
        else:
            plaintext = self.decrypt_default_key(text)
        print("Final text is: {}".format(plaintext))
        return plaintext

    def decrypt_auto_key(self, text: str):
        if not self.extended:
            text = text.upper()
            self.key = self.key.upper()
        # decrypt
        plaintext = ""
        key_len = len(self.key)
        for i in range(key_len):
            search_key = np.where(self.matrix[:, 0] == self.key[i])
            idx_key = search_key[0][0]
            search_cipher = np.where(self.matrix[idx_key] == text[i])
            idx_cipher = search_cipher[0][0]
            plaintext += self.matrix[0][idx_cipher]

        key_pos = 0
        for i in range(key_len, len(text)):
            search_key = np.where(self.matrix[:, 0] == plaintext[key_pos])
            idx_key = search_key[0][0]
            search_cipher = np.where(self.matrix[idx_key] == text[i])
            idx_cipher = search_cipher[0][0]
            plaintext += self.matrix[0][idx_cipher]
            key_pos += 1
        plaintext = [ord(x) for x in plaintext]
        return plaintext

    def decrypt_default_key(self, text: str):
        if not self.extended:
            text = text.upper()
            self.key = self.key.upper()

        # expand key to encrypt plain text
        expanded_key = self.expand_key(text)
        # decrypt
        key_pos = 0
        plaintext = []
        for letter in text:
            search_key = np.where(self.matrix[:, 0] == expanded_key[key_pos])
            idx_key = search_key[0][0]
            search_cipher = np.where(self.matrix[idx_key] == letter)
            idx_cipher = search_cipher[0][0]
            if self.matrix[0][idx_cipher] == '':
                plaintext.append(0)
            else:
                plaintext.append(ord(self.matrix[0][idx_cipher]))
            key_pos += 1
        return plaintext
