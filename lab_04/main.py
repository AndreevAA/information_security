import sys
from base64 import *
from random import randrange
from Crypto.Util.number import inverse


class RSA(object):
    def __init__(self, p, q):
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = self.get_e(self.phi)
        self.d = self.get_d(self.e, self.phi)

    def crypt(self, char, key):
        return char ** key % self.n

    def encrypt_string(self, string):
        result = ""
        for char in string:
            current_char = self.crypt(ord(char), self.e)
            result += chr(current_char)
        return result

    def decrypt_string(self, string):
        result = ""
        for char in string:
            current_char = self.crypt(ord(char), self.d)
            result += chr(current_char)
        return result

    def euclid(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def get_d(self, e, phi):
        return inverse(e, phi)

    def get_e(self, phi):
        while True:
            result = randrange(2, phi)
            if self.euclid(result, phi) == 1:
                return result


if __name__ == '__main__':

    if len(sys.argv) < 2:
        source_str = "я так люблю учиться в МГТУ!!!"
        print("Source: ", source_str)

        rsa = RSA(p=199, q=179)

        encoded = b64encode(source_str.encode("UTF-8")).decode('ascii')
        rsa_decoded = rsa.encrypt_string(encoded)
        print("Encrypted: ", rsa_decoded)

        decrypted_rsa = rsa.decrypt_string(rsa_decoded)
        decoded = b64decode(decrypted_rsa)
        print("Decrypted: ", decoded.decode("UTF-8"))
    else:
        filename = sys.argv[1]
        with open(filename, 'rb') as input_file:
            data = input_file.read()
            rsa = RSA(p=199,q=179)

            source_str = b32encode(data)
            decoded_str = source_str.decode("ascii")
            print("Encrypting...")

            encrypted = rsa.encrypt_string(decoded_str)
            with open("encrypted_" + filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted.encode())
                encrypted_file.close()
            print("Decrypting...")

            decrypted = rsa.decrypt_string(encrypted)
            restored = b32decode(decrypted)
            with open("decrypted_" + filename, 'wb') as restored_file:
                restored_file.write(restored)
                restored_file.close()
