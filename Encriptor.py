import gettext
import base64
import random
from typing import Callable, Any
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

_ = gettext.gettext


class Encryptor:
    '''
    A class to encrypt/decrypt text using AES algorithm with 256 bits password based key
    derivation using salt bytes and pbkdf2 algorithm.
    '''
    BLOCK_SIZE: int = 16
    SALT_SIZE: int = 16

    #  pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    Pad: Callable[[Any], Any] = lambda s: s + (Encryptor.BLOCK_SIZE - len(s.encode('utf-8')) % Encryptor.BLOCK_SIZE) \
                                          * chr(Encryptor.BLOCK_SIZE - len(s.encode('utf-8')) % Encryptor.BLOCK_SIZE)

    Unpad: Callable[[Any], Any] = lambda s: s[:-ord(s[len(s) - 1:])]

    '''
    @param password: Password in plain text. type: str    
    @param salt: Salt bytes. type: bytes. 
                 Note: If 'None' a random array of bytes will be generated.    
    @return: Returns the generated key (32 bytes) and the used salt bytes
    '''

    @staticmethod
    def Get_Private_Key(password: str, salt: bytes = None) -> tuple:
        if salt is None:
            salt = random.randbytes(Encryptor.SALT_SIZE)  # b"this is a salt"

        # salt must have right size
        if len(salt) != Encryptor.SALT_SIZE:
            raise Exception(_("Salt must have {} bytes.").format(Encryptor.SALT_SIZE))

        kdf = PBKDF2(password, salt, 64, 1000)
        key = kdf[:32]  # return 32 bytes (256 bits) key
        return key, salt

    @staticmethod
    def Encrypt(raw: str, password: str) -> str:
        private_key, salt = Encryptor.Get_Private_Key(password)
        raw = Encryptor.Pad(raw).encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        result = ""
        try:
            encbytes: bytes = cipher.encrypt(raw)
            result = base64.b64encode(salt + iv + encbytes).decode('utf-8')
        except:
            print("encrypt failed!")

        return result
        # return base64.b64encode(salt + iv + cipher.encrypt(raw)).decode('utf-8')

    @staticmethod
    def Decrypt(enc: str, password: str) -> (str, bool):
        """
        :param enc: Encrypted text
        :type enc: String (str)
        :param password: Password in plain text
        :type password: String (str)
        :return: Returns the decrypted text and the process state (True if succeeded, False otherwise)
        :rtype: tuple(str, bool)
        """
        state = False
        enc = base64.b64decode(enc.encode('utf-8'))  # get bytes
        salt = enc[0:Encryptor.SALT_SIZE]
        private_key, salt = Encryptor.Get_Private_Key(password, salt)
        start_content: int = Encryptor.SALT_SIZE + Encryptor.BLOCK_SIZE
        iv = enc[Encryptor.SALT_SIZE:start_content]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        result: str = ""
        try:
            decbytes = cipher.decrypt(enc[start_content:])
            result = bytes.decode(Encryptor.Unpad(decbytes))
            state = len(result) > 0
        except:
            print("decrypt failed!")

        return result, state
        # return bytes.decode(Encryptor.Unpad(cipher.decrypt(enc[start_content:])))
