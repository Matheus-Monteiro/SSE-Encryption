import rsa
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

class Criptography:
    def encrypt(self, data, algorithm):
        encrypter = self._get_encrypter(algorithm)
        return encrypter(data)

    def decrypt(self, data, algorithm):
        decrypter = self._get_decrypter(algorithm)
        return decrypter(data)
    
    def _get_encrypter(self, algorithm):
        if algorithm == 'RSA':
            return self._encrypt_rsa
        elif algorithm == 'AES':
            return self._encrypt_aes
        else:
            raise ValueError(algorithm)
    
    def load_keys(self, publicKeyStr, privateKeyStr):
        publicKeyByte = base64.b64decode(publicKeyStr.encode())
        privateKeyByte = base64.b64decode(privateKeyStr.encode())

        publicKey = rsa.PublicKey.load_pkcs1(publicKeyByte)
        privateKey = rsa.PrivateKey.load_pkcs1(privateKeyByte)

        return publicKey, privateKey

    def read_keys(self):
        with open('publicKey.txt', "r") as f:
            decodedPublicKey = f.read()
        with open('privateKey.txt', "r") as f:
            decodedPrivateKey = f.read()
        return self.load_keys(decodedPublicKey, decodedPrivateKey)

    def read_master_key(self):
        with open('masterKey.txt', "r") as f:
            MK = f.read()
        return MK

    def _get_decrypter(self, algorithm):
        if algorithm == 'RSA':
            return self._decrypt_rsa
        elif algorithm == 'AES':
            return self._decrypt_aes
        else:
            raise ValueError(algorithm)

    def _encrypt_rsa(self, data):
        decodedPublicKey, decodedPrivateKey = self.read_keys()
        encrypted_data = rsa.encrypt(data.encode(), decodedPublicKey)
        base64_encrypted_message = base64.b64encode(encrypted_data)
        return str(base64_encrypted_message)[
        2:-1
        ]

    def _decrypt_rsa(self, data):
        decodedPublicKey, decodedPrivateKey = self.read_keys()
        ciphertext = base64.b64decode(data.encode())
        return rsa.decrypt(ciphertext, decodedPrivateKey).decode()

    def _encrypt_aes(self, data):
        MK = self.read_master_key().encode()
        aes = AES.new(MK, AES.MODE_ECB)
        data = pad(data.encode(),16)
        print(data)
        encrypted_data = aes.encrypt(data)
        base64_encrypted_message = base64.b64encode(encrypted_data)
        print(base64_encrypted_message)
        return str(base64_encrypted_message)[
        2:-1
        ]

    def _decrypt_aes(self, data):
        MK = self.read_master_key().encode()
        ciphertext = base64.b64decode(data.encode())
        print(ciphertext)
        aes = AES.new(MK, AES.MODE_ECB)
        return unpad(aes.decrypt(ciphertext),16).decode()