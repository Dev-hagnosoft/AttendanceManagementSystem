import bcrypt
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import uuid


def hash_password(plaintext_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def generateUniqueKey():
    uniquekey = str(uuid.uuid4())
    return uniquekey


def checkPassword (text_password,hashed_password):
    if bcrypt.checkpw(text_password.encode('utf-8'), hashed_password.encode('utf-8')):
        return 1
    else:
        return 0

keynam_encrypt= "oebb8c24dw9f75c9"

def encrypt (text):
    obj_crypt= Crypt()
    encrypted_text= obj_crypt.encrypt(text,keynam_encrypt)
    return  encrypted_text

def dcrypt (en_text):
    obj_crypt= Crypt()
    encrypted_text= obj_crypt.decrypt(en_text,keynam_encrypt)
    return  encrypted_text


class Crypt:
    def __init__(self, salt='fc35-8426-34de0b'):
        self.salt = salt.encode('utf8')
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf-8'), AES.MODE_CFB, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc.encode('utf8'))
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

    def decrypt(self, enc_str, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf8'), AES.MODE_CFB, self.salt)
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError('Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError('Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

