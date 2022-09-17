"""
工具类
"""
import hashlib
import base64
import pickle
from global_config import config

__all__ = [
    "PasswordHandler"
]


class PasswordHandler:
    """
    密码处理器
    """

    @classmethod
    def encode(cls, plaintext: str) -> str:
        """
        加密
        :param plaintext: 明文
        :return:
        """
        # todo: 支持加盐
        if config.encryption_algorithm == 'md5':
            return cls.md5_encode(plaintext)
        elif config.encryption_algorithm == 'base64':
            return cls.base64_encode(plaintext)
        else:
            return cls.sha256_encode(plaintext)

    @classmethod
    def decode(cls, ciphertext: str):
        """
        解密（只有RSA可以解密）
        :param ciphertext: 密文
        :return:
        """
        if config.encryption_algorithm == 'md5':
            return ciphertext
        elif config.encryption_algorithm == 'base64':
            return cls.base64_decode(ciphertext)
        else:
            return ciphertext

    @classmethod
    def sha256_encode(cls, plaintext: str) -> str:
        return hashlib.sha256(plaintext.encode('utf-8')).hexdigest()

    @classmethod
    def md5_encode(cls, plaintext: str) -> str:
        return hashlib.md5(plaintext.encode('utf-8')).hexdigest()

    @classmethod
    def base64_encode(cls, plaintext: str) -> str:
        return base64.b64encode(plaintext.encode('utf8')).decode()

    @classmethod
    def base64_decode(cls, ciphertext: str) -> str:
        return base64.b64decode(ciphertext.encode('utf8')).decode()

    @classmethod
    def serialization(cls, obj) -> str:
        """
        序列化对象
        :param obj: 对象
        :return: 序列化后的对象
        """
        return base64.b64encode(pickle.dumps(obj)).decode()

    @classmethod
    def deserialize(cls, obj):
        """
        反序列化对象
        :param obj: 对象
        :return: 反序列化后的对象
        """
        return pickle.loads(base64.b64decode(obj.encode()))
