def encrypt(plaintext, key):
    '''
    For encrypting plaintext with Vignere Cipher
    '''
    ciphertext = ""
    for i in range(len(plaintext)):
        c_val = chr(
            (ord(plaintext[i]) + ord(key[i % len(key)]) - 2 * ord('A')) % 26 + ord('A')
        )
        ciphertext += c_val

    return ciphertext


def decrypt(ciphertext, key):
    '''
    For decrypting plaintext with Vignere Cipher
    '''
    plaintext = ""
    for i in range(len(ciphertext)):
        c_val = chr(
            (ord(ciphertext[i]) - ord(key[i % len(key)])) % 26 + ord('A')
        )
        plaintext += c_val

    return plaintext
