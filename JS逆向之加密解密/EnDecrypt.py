# encoding: utf-8
from hashlib import md5
from hashlib import sha1
import hmac
import base64
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.Cipher import DES
from pyDes import des, CBC, ECB, PAD_PKCS5
import rsa


class EnDecryptPublicFunction:

    @staticmethod
    def clean_char(str_text):
        b_char_list = [
            b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05',
            b'\x06', b'\x07', b'\x08', b'\x09', b'\n']
        for b_char in b_char_list:
            str_text = str_text.replace(b_char.decode(), "")
        return str_text

    @staticmethod
    def fill_text(str_text):
        """字符串补成8的倍数"""
        num_0 = len(str_text) % 8
        if num_0 != 0:
            str_text = str_text + '\0' * (8 - num_0)
        return str_text


class Base64Md5Sha1HmacUtil:

    @staticmethod
    def base64_encrypt_text(decrypt_text: str) -> str:
        """
        Bse64加密
        :param decrypt_text: 明文
        :return: 密文
        """
        return base64.b64encode(decrypt_text.encode("utf-8")).decode()

    @staticmethod
    def base64_decrypt_text(encrypt_text: str) -> str:
        """
        Bse64解密
        :param encrypt_text: 密文
        :return: 明文
        """
        return base64.b64decode(encrypt_text).decode("utf-8")

    @staticmethod
    def md5_encrypt_text(decrypt_text: str) -> str:
        """
        md5加密
        :param decrypt_text: 明文
        :return: 密文
        """
        return md5(decrypt_text.encode('utf8')).hexdigest()

    @staticmethod
    def sha1_encrypt_text(decrypt_text: str) -> str:
        """
        SHA1加密
        :param decrypt_text: 明文
        :return: 密文
        """
        return sha1(decrypt_text.encode('utf8')).hexdigest()

    @staticmethod
    def hmac_encrypt_text(decrypt_text: str, key: str) -> str:
        """
        SHA1加密
        :param decrypt_text: 明文
        :param key: 密钥
        :return: 密文
        """
        mac = hmac.new(key.encode('utf-8'), decrypt_text.encode('utf-8'), md5)
        return mac.hexdigest()


class AesUtil:

    @staticmethod
    def aes_encrypt_text(decrypt_text: str, key: str, iv="", model="CBC") -> str:
        """
        AES加密
        :param decrypt_text: 明文
        :param key: 密钥
        :param model: 加密模式： CBC, ECB
        :param iv: 密钥偏移量，只有CBC模式有
        :return: 密文
        """
        if model == 'CBC':
            aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        else:
            aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        encrypt_text = aes.encrypt(pad(decrypt_text.encode('utf-8'), AES.block_size, style='pkcs7'))
        encrypt_text = base64.b64encode(encrypt_text).decode()
        return encrypt_text

    @staticmethod
    def aes_decrypt_text(encrypt_text: str, key: str, iv="", model="CBC") -> str:
        """
        AES解密
        :param encrypt_text: 密文
        :param key: 密钥
        :param model: 解密模式： CBC, ECB
        :param iv: 密钥偏移量，只有CBC模式有
        :return:解密后的数据
        """
        if model == 'CBC':
            aes = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        else:
            aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        decrypt_text = aes.decrypt(base64.b64decode(encrypt_text)).decode('utf8')
        return EnDecryptPublicFunction.clean_char(decrypt_text)


class DesUtil:

    @staticmethod
    def des_encrypt_text(decrypt_text: str, key: str, iv="", model="CBC") -> str:
        """
        DES加密
        :param decrypt_text: 明文
        :param key: 密钥
        :param model: 加密模式： CBC, ECB
        :param iv: 密钥偏移量
        :return: 加密后的数据
        """
        if model == 'CBC':
            des_obj = des(key[:8].encode('utf-8'), CBC, iv.encode('utf-8'), padmode=PAD_PKCS5)
        else:
            des_obj = des(key[:8].encode('utf-8'), ECB, padmode=PAD_PKCS5)
        encrypt_text = des_obj.encrypt(decrypt_text.encode('utf-8'))
        encrypt_text = base64.b64encode(encrypt_text).decode()
        return encrypt_text

    @staticmethod
    def des_decrypt_text(encrypt_text: str, key: str, iv="", model="CBC") -> str:
        """
        DES解密
        :param encrypt_text: 密文
        :param key: 秘钥
        :param model: 解密模式： CBC, ECB
        :param iv:秘钥偏移量
        :return:解密后的数据
        """
        if model == 'CBC':
            des_obj = des(key[:8].encode('utf-8'), CBC, iv.encode('utf-8'), padmode=PAD_PKCS5)
        else:
            des_obj = des(key[:8].encode('utf-8'), ECB, padmode=PAD_PKCS5)
        decrypt_text = des_obj.decrypt(base64.b64decode(encrypt_text)).decode('utf8')
        return EnDecryptPublicFunction.clean_char(decrypt_text)


class Des3Util:

    @staticmethod
    def des3_encrypt_text(decrypt_text: str, key: str, iv="", model="CBC") -> str:
        """
        DES3加密
        :param decrypt_text: 明文
        :param key: 密钥
        :param model: 加密模式： CBC, ECB
        :param iv: 密钥偏移量
        :return: 加密后的数据
        """
        if model == 'CBC':
            des3 = DES3.new(key.encode('utf-8'), DES3.MODE_CBC, iv[:8].encode('utf-8'))
        else:
            des3 = DES3.new(key.encode('utf-8'), DES3.MODE_ECB)
        encrypt_text = des3.encrypt(pad(decrypt_text.encode('utf-8'), DES3.block_size, style='pkcs7'))
        encrypt_text = base64.b64encode(encrypt_text).decode()
        return encrypt_text

    @staticmethod
    def des3_decrypt_text(encrypt_text: str, key: str, iv="", model="CBC") -> str:
        """
        DES3解密
        :param encrypt_text: 密文
        :param key: 秘钥
        :param model: 解密模式： CBC, ECB
        :param iv:秘钥偏移量
        :return:解密后的数据
        """
        if model == 'CBC':
            des3 = DES3.new(key.encode('utf-8'), DES3.MODE_CBC, iv[:8].encode('utf-8'))
        else:
            des3 = DES3.new(key.encode('utf-8'), DES3.MODE_ECB)
        decrypt_text = des3.decrypt(base64.b64decode(encrypt_text)).decode('utf8')
        return EnDecryptPublicFunction.clean_char(decrypt_text)


class PyDesUtil:

    @staticmethod
    def des_encrypt_text(decrypt_text: str, key: str, iv="", model="CBC") -> str:
        """
        DES加密
        :param decrypt_text: 明文
        :param key: 密钥
        :param model: 加密模式： CBC, ECB
        :param iv: 密钥偏移量
        :return: 加密后的数据
        """
        if model == 'CBC':
            des_obj = DES.new(key[:8].encode('utf-8'), DES.MODE_CBC, iv.encode('utf-8'))
        else:
            des_obj = DES.new(key[:8].encode('utf-8'), DES.MODE_ECB)
        encrypt_text = des_obj.encrypt(pad(decrypt_text.encode('utf-8'), DES3.block_size, style='pkcs7'))
        encrypt_text = base64.b64encode(encrypt_text).decode()
        return encrypt_text

    @staticmethod
    def des_decrypt_text(encrypt_text: str, key: str, iv="", model="CBC") -> str:
        """
        DES解密
        :param encrypt_text: 密文
        :param key: 秘钥
        :param model: 解密模式： CBC, ECB
        :param iv:秘钥偏移量
        :return:解密后的数据
        """
        if model == 'CBC':
            des_obj = DES.new(key[:8].encode('utf-8'), DES.MODE_CBC, iv.encode('utf-8'))
        else:
            des_obj = DES.new(key[:8].encode('utf-8'), DES.MODE_ECB)
        decrypt_text = des_obj.decrypt(base64.b64decode(encrypt_text)).decode('utf8')
        return EnDecryptPublicFunction.clean_char(decrypt_text)


class RsaUtil:

    @staticmethod
    def rsa_encrypt_text(public_key, decrypt_text: str) -> str:
        """
        RSA加密
        :param public_key:  公钥
        :param decrypt_text: 明文
        :return: 加密后的数据
        """
        encrypt_text = rsa.encrypt(decrypt_text.encode('utf-8'), rsa.PublicKey.load_pkcs1(public_key))
        encrypt_text = base64.b64encode(encrypt_text).decode()
        return encrypt_text

    @staticmethod
    def rsa_decrypt_text(private_key, encrypt_text: str) -> str:
        """
        RSA解密
        :param private_key: 私钥
        :param encrypt_text: 密文
        :return: 明文
        """
        decrypt_text = rsa.decrypt(base64.b64decode(encrypt_text), rsa.PrivateKey.load_pkcs1(private_key)).decode('utf8')
        return decrypt_text

    @staticmethod
    def rsa_sign(private_key, decrypt_text, method="MD5"):
        """
        rsa签名
        :param private_key: 私钥
        :param decrypt_text: 明文
        :param method: 'MD5', 'SHA-1','SHA-224', SHA-256', 'SHA-384' or 'SHA-512'
        :return:
        """
        sign_text = rsa.sign(decrypt_text.encode('utf-8'), rsa.PrivateKey.load_pkcs1(private_key), method)
        sign_text = base64.b64encode(sign_text).decode()
        return sign_text

    @staticmethod
    def rsa_verify(signature, public_key, decrypt_text):
        """
        rsa验签
        :param signature: rsa签名
        :param public_key: 公钥
        :param decrypt_text: 明文
        :return:
        """
        return rsa.verify(decrypt_text.encode('utf-8'), base64.b64decode(signature), rsa.PublicKey.load_pkcs1(public_key))


if __name__ == "__main__":
    _object = AesUtil()
    # AES_CBC解密模式
    import re
    encrypt_str = "XP8AMyYnBvtWtrx5guiKmbLHNPXXTco8uMIhDkLH03OjD7CSvc1yqdUs6JSGD97UcjVhiu4d75vv3teFiFtDFbicAW1Wp+W6b7tjTYfPJpetM8KG9heuvDn2NhglJMv9chdBpxaD9l30Na27U2D1sw=="
    key_str = 'abcdef0123456789'
    iv_str = '0123456789abcdef'
    decrypt_str = _object.aes_decrypt_text(encrypt_str, key_str, iv_str)
    print("AES_CBC解密:", re.sub(r"\S{8}-\S{4}-\S{4}-\S{4}-\S{12}", "", decrypt_str))
    # AES_CBC加密模式
    decrypt_str = '{"Type":0,"page":3,"expire":1596461032894}'
    key_str = "55b3b62613aef1a0"
    iv_str = "55b3b62613aef1a0"
    encrypt_str = _object.aes_encrypt_text(decrypt_str, key_str, iv_str)
    print(f"AES_CBC加密: {encrypt_str}")
    # AES_CBC解密模式
    encrypt_str = "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"
    key_str = "0a1fea31626b3b55"
    iv_str = "0a1fea31626b3b55"
    decrypt_str = _object.aes_decrypt_text(encrypt_str, key_str, iv_str).replace("", "")
    print(f"AES_CBC解密: {decrypt_str}")

    # AES_ECB加密模式
    list_url = "http://ggzy.xzsp.tj.gov.cn:80/jyxxcggg/948709.jhtml"
    ccc = re.search(r"(\d+)\.jhtml", list_url).group(1)
    decrypt_str = str(ccc)
    key_str = "qnbyzzwmdgghmcnm"
    encrypt_str = _object.aes_encrypt_text(decrypt_str, key_str, model="ECB")
    print(f"AES_ECB加密: {list_url.replace(decrypt_str, encrypt_str.replace('/', '^')[:-2])}")
    decrypt_str = _object.aes_decrypt_text(encrypt_str, key_str, model="ECB")
    print(f"AES_ECB解密: {decrypt_str}")

    print("+++++++++++++++++++++++++=======================================================")
    _object = DesUtil()  # 使用Crypto里面的DES库
    _object2 = PyDesUtil()  # 使用PyDes库
    # DES_CBC加密解密模式
    import json
    param = {"appId": "cf997823ce9425ec88a91bba9c188ca5", "method": "GETDATA", "timestamp": 1599713841621, "clienttype": "WEB", "object": {"city": "杭州"}, "secret": "1c55273cdbb5c59872f74d9bb90484b7"}
    decrypt_str = json.dumps(param, separators=(',', ':'))
    key_str = "86b4104a75dd865f"
    iv_str = "bcefc965"
    encrypt_str = _object.des_encrypt_text(decrypt_str, key_str, iv_str)
    print(f"DES_CBC加密: {encrypt_str}")
    decrypt_str = _object.des_decrypt_text(encrypt_str, key_str, iv_str)
    print(f"DES_CBC解密: {decrypt_str}")
    encrypt_str = _object2.des_encrypt_text(decrypt_str, key_str, iv_str)
    print(f"DES_CBC加密: {encrypt_str}")
    decrypt_str = _object2.des_decrypt_text(encrypt_str, key_str, iv_str)
    print(f"DES_CBC解密: {decrypt_str}")

    # DES_ECB加密解密模式
    decrypt_str = "这是一个DES_ECB加密解密模式测试4"
    key_str = "7hyu1o2k"
    encrypt_str = _object.des_encrypt_text(decrypt_str, key_str, model="ECB")
    print(f"DES_ECB加密: {encrypt_str}")
    decrypt_ = _object.des_decrypt_text(encrypt_str, key_str, model="ECB")
    print(f"DES_ECB解密: {decrypt_}")
    encrypt_str = _object2.des_encrypt_text(decrypt_str, key_str, model="ECB")
    print(f"DES_ECB加密: {encrypt_str}")
    decrypt_ = _object2.des_decrypt_text(encrypt_str, key_str, model="ECB")
    print(f"DES_ECB解密: {decrypt_}")

    print("+++++++++++++++++++++++++=======================================================")
    # DES3_CCB加密解密模式
    _object = Des3Util()
    decrypt_str = "这是一个DES3_CBC加密解密测"
    key_str = "7hyu1o2kuytg65ws"
    iv_str = "hyr0mfzf"
    encrypt_str = _object.des3_encrypt_text(decrypt_str, key_str, iv_str)
    print(f"DES3_CBC加密: {encrypt_str}")
    decrypt_ = _object.des3_decrypt_text(encrypt_str, key_str, iv_str)
    print(f"DES3_CBC解密: {decrypt_}")
    # DES3_ECB加密解密模式
    _object = Des3Util()
    decrypt_str = "这是一个DES3_ECB加密解密模式测试"
    key_str = "7hyu1o2kuytg65ws"
    encrypt_str = _object.des3_encrypt_text(decrypt_str, key_str, model="ECB")
    print(f"DES3_ECB加密: {encrypt_str}")
    decrypt_ = _object.des3_decrypt_text(encrypt_str, key_str, model="ECB")
    print(f"DES3_ECB解密: {decrypt_}")

    print("+++++++++++++++++++++++++=======================================================")
    _object = RsaUtil()
    # rsa加密解密
    privateKey = '''-----BEGIN RSA PRIVATE KEY----- 
    MIICXgIBAAKBgQDZAzJb0n62WqMKQUFBdIBUc8Ld8NKuK1nrd9xXVrqt/UwXQlYn MuGc8M1+c4rhRMZHcG1a4RBwUZBjQSWFSf9RdYAMHdyncmiHeTcAExZJC8jN8DrR arbcJqPPPFPSsCMoRh9mxZESLJPikJjUCEdZvBYKXbMtiW5y3eefR6U2WQIDAQAB AoGBAL1NtZM11sUZ4ZmjfNotV3jUFovmdNHsDR+DylkB1gzKpaKwgljlYLu3r3p8 Lgz+InzVDP+2ztE7xVlfzewstaNtRF/P32DI1J+zkK8tvW9jJ1Qj3kBIBeS6adn2 iWeMzcA4hNSekNPj3OXl8ZlsQHcwM+U0WoJV6t6nHF3dMMyBAkEA7KzVGFW5CgBn OLITLbtMCpWgLeL7Cz5ZVZ/0bWOQ8L4Tl2h64XmPCLFWlmIWN1o8ndncfrb7r2BG Y1QJcaNiyQJBAOq7XEuB9TMwXl6L8YdY18Ejve9TrTy8B9m9b++SeYYpKmrQrGxX KOpSY6CV3W04fTdnv3GSeMD1wwqC3oUC7xECQQDAREd41WrU7S7tp/xckmNb1eGi ZVp779Ky9JakptYAPOm9fmsU8KN59FbbJCPYI75Kncm6Rvx/pD6KQqLJZmnBAkEA uLeqYM0rHRZCHRr5fa4fUyECVbS+jh3V+7ZEwP2+XiJE+/usxDEuxH8DYZqtvkaG 2zPshr5iAk8kJkBoRbnSUQJAbS97Id1Beq/rejivApjKTP2lCfkOj4TbluNspiec rs7Eac1FTIFOwD+6tMG3K7nuRQ1UB9Cltjy15XW8MmYHRA== 
    -----END RSA PRIVATE KEY----- '''
    publicKey = '''-----BEGIN RSA PUBLIC KEY----- 
    MIGJAoGBANkDMlvSfrZaowpBQUF0gFRzwt3w0q4rWet33FdWuq39TBdCVicy4Zzw zX5ziuFExkdwbVrhEHBRkGNBJYVJ/1F1gAwd3KdyaId5NwATFkkLyM3wOtFqttwm o888U9KwIyhGH2bFkRIsk+KQmNQIR1m8Fgpdsy2JbnLd559HpTZZAgMBAAE= 
    -----END RSA PUBLIC KEY----- '''
    decrypt_str = "nihao@456"
    encrypt_str = _object.rsa_encrypt_text(publicKey, decrypt_str)
    print(f"RSA加密: {encrypt_str}")
    decrypt_str = _object.rsa_decrypt_text(privateKey, encrypt_str)
    print(f"RSA解密: {decrypt_str}")
    sign = _object.rsa_sign(privateKey, decrypt_str)
    print(f"RSA签名: {sign}")
    verify_sign = _object.rsa_verify(sign, publicKey, decrypt_str)
    print(f"RSA验签: {verify_sign}")

    print("+++++++++++++++++++++++++=======================================================")
    _object = Base64Md5Sha1HmacUtil()
    # base64解密
    encrypt_str = "eyJzdWNjZXNzIjp0cnVlLCJlcnJjb2RlIjowLCJlcnJtc2ciOiJzdWNjZXNzIiwicmVzdWx0Ijp7InN1Y2Nlc3MiOnRydWUsImRhdGEiOnsiY2l0eWluZm8iOnsiY2l0eWdpZCI6IjkxIiwiY2l0eWlkIjoiMTAxMjEwMTAxIiwiY2l0eW5hbWUiOiJcdTY3NmRcdTVkZGUiLCJwcm92aW5jZW5hbWUiOiJcdTZkNTlcdTZjNWYiLCJyYW5rZmxhZyI6IjEiLCJyYW5rZmxhZ18xNjkiOiIxIn0sImFxaSI6eyJjaXR5IjoiXHU2NzZkXHU1ZGRlIiwidGltZSI6IjIwMjAtMDktMTAgMDc6MDA6MDAiLCJhcWkiOiI5NyIsInBtMl81IjoiNzIiLCJwbTEwIjoiMTI1Iiwic28yIjoiNy4wMDAiLCJubzIiOiI3NS4wMDAiLCJvMyI6IjIyLjAwMCIsIm8zXzhoIjoiMC4wMDAiLCJjbyI6IjEuMDAwIiwicmFuayI6IjMyNiIsImxldmVsIjoiXHU0ZThjXHU3ZWE3IiwicXVhbGl0eSI6Ilx1ODI2ZiIsInByaW1hcnlfcG9sbHV0YW50IjoiUE0yLjUiLCJkYXlfYXFpIjoiOTMiLCJkYXlfcG9sbCI6IlBNMi41IiwiZGF5X2NvbXBsZXgiOiI1LjgxMCIsIjc0Y29tcGxleHJhbmsiOiI3NCIsImNvbXBsZXhyYW5rIjoiMzI4IiwiMTY5Y29tcGxleHJhbmsiOiIxNjYifSwicm93cyI6W3sidGltZSI6IjIwMjAtMDktMTAgMDc6MDA6MDAiLCJjaXR5bmFtZSI6Ilx1Njc2ZFx1NWRkZSIsInBvaW50Z2lkIjoiMjI3IiwicG9pbnRuYW1lIjoiXHU2ZDU5XHU2YzVmXHU1MTljXHU1OTI3IiwicG9pbnRsZXZlbCI6Ilx1NTZmZFx1NjNhN1x1NzBiOSIsInJlZ2lvbiI6Ilx1NmM1Zlx1NWU3Mlx1NTMzYSIsImxhdGl0dWRlIjoiMzAuMjY5MjAwIiwibG9uZ2l0dWRlIjoiMTIwLjE5MDAwMCIsImFxaSI6IjEzNCIsInpxX2FxaSI6IjAiLCJwbTJfNSI6IjEwMiIsInBtMTAiOiIxNjkiLCJzbzIiOiIxMCIsIm5vMiI6IjEwNiIsImNvIjoiMS4zMDAiLCJvMyI6IjEyIiwiY29tcGxleGluZGV4IjoiOC41NDUyMzgxIiwibGV2ZWwiOiJcdTRlMDlcdTdlYTciLCJxdWFsaXR5IjoiXHU4ZjdiXHU1ZWE2XHU2YzYxXHU2N2QzIiwicHJpbWFyeV9wb2xsdXRhbnQiOiJQTTIuNSIsInJhdGlvIjowLjE3NTQsImluZGV4cmF0aW8iOjAuMDUyNDAwMDAwMDAwMDAwMDAyfSx7InRpbWUiOiIyMDIwLTA5LTEwIDA3OjAwOjAwIiwiY2l0eW5hbWUiOiJcdTY3NmRcdTVkZGUiLCJwb2ludGdpZCI6IjIyNSIsInBvaW50bmFtZSI6Ilx1NGUwYlx1NmM5OSIsInBvaW50bGV2ZWwiOiJcdTU2ZmRcdTYzYTdcdTcwYjkiLCJyZWdpb24iOiJcdTZjNWZcdTVlNzJcdTUzM2EiLCJsYXRpdHVkZSI6IjMwLjMwNTgwMCIsImxvbmdpdHVkZSI6IjEyMC4zNDgwMDAiLCJhcWkiOiIxMTgiLCJ6cV9hcWkiOiIwIiwicG0yXzUiOiI4OSIsInBtMTAiOiIxODUiLCJzbzIiOiIxMiIsIm5vMiI6IjczIiwiY28iOiIxLjEwMCIsIm8zIjoiMjAiLCJjb21wbGV4aW5kZXgiOiI3LjYxMDcxNDMiLCJsZXZlbCI6Ilx1NGUwOVx1N2VhNyIsInF1YWxpdHkiOiJcdThmN2JcdTVlYTZcdTZjNjFcdTY3ZDMiLCJwcmltYXJ5X3BvbGx1dGFudCI6IlBNMTAiLCJyYXRpbyI6MCwiaW5kZXhyYXRpbyI6MC4wMjR9LHsidGltZSI6IjIwMjAtMDktMTAgMDc6MDA6MDAiLCJjaXR5bmFtZSI6Ilx1Njc2ZFx1NWRkZSIsInBvaW50Z2lkIjoiMjI4IiwicG9pbnRuYW1lIjoiXHU2NzFkXHU2NjU2XHU0ZTk0XHU1MzNhIiwicG9pbnRsZXZlbCI6Ilx1NTZmZFx1NjNhN1x1NzBiOSIsInJlZ2lvbiI6Ilx1NGUwYlx1NTdjZVx1NTMzYSIsImxhdGl0dWRlIjoiMzAuMjg5NzAwIiwibG9uZ2l0dWRlIjoiMTIwLjE1NzAwMCIsImFxaSI6IjEwOCIsInpxX2FxaSI6IjAiLCJwbTJfNSI6IjgxIiwicG0xMCI6IjE0NiIsInNvMiI6IjEwIiwibm8yIjoiMTIwIiwiY28iOiIxLjEwMCIsIm8zIjoiMTEiLCJjb21wbGV4aW5kZXgiOiI3LjkxMDQxNjciLCJsZXZlbCI6Ilx1NGUwOVx1N2VhNyIsInF1YWxpdHkiOiJcdThmN2JcdTVlYTZcdTZjNjFcdTY3ZDMiLCJwcmltYXJ5X3BvbGx1dGFudCI6IlBNMi41IiwicmF0aW8iOjAuMDU4Nzk5OTk5OTk5OTk5OTk4LCJpbmRleHJhdGlvIjowLjAxOTU5OTk5OTk5OTk5OTk5OX0seyJ0aW1lIjoiMjAyMC0wOS0xMCAwNzowMDowMCIsImNpdHluYW1lIjoiXHU2NzZkXHU1ZGRlIiwicG9pbnRnaWQiOiIyMzEiLCJwb2ludG5hbWUiOiJcdTU3Y2VcdTUzYTJcdTk1NDciLCJwb2ludGxldmVsIjoiXHU1NmZkXHU2M2E3XHU3MGI5IiwicmVnaW9uIjoiXHU4NDI3XHU1YzcxXHU1MzNhIiwibGF0aXR1ZGUiOiIzMC4xODE5MDAiLCJsb25naXR1ZGUiOiIxMjAuMjcwMDAwIiwiYXFpIjoiMTAwIiwienFfYXFpIjoiMCIsInBtMl81IjoiNzUiLCJwbTEwIjoiMTE2Iiwic28yIjoiNiIsIm5vMiI6Ijc5IiwiY28iOiIwLjkwMCIsIm8zIjoiMzYiLCJjb21wbGV4aW5kZXgiOiI2LjMyNTAwMDAiLCJsZXZlbCI6Ilx1NGU4Y1x1N2VhNyIsInF1YWxpdHkiOiJcdTgyNmYiLCJwcmltYXJ5X3BvbGx1dGFudCI6IlBNMi41IiwicmF0aW8iOi0wLjAyOTEwMDAwMDAwMDAwMDAwMSwiaW5kZXhyYXRpbyI6LTAuMDAyNzAwMDAwMDAwMDAwMDAwMX0seyJ0aW1lIjoiMjAyMC0wOS0xMCAwNzowMDowMCIsImNpdHluYW1lIjoiXHU2NzZkXHU1ZGRlIiwicG9pbnRnaWQiOiIyMjIiLCJwb2ludG5hbWUiOiJcdTZlZThcdTZjNWYiLCJwb2ludGxldmVsIjoiXHU1NmZkXHU2M2E3XHU3MGI5IiwicmVnaW9uIjoiXHU2ZWU4XHU2YzVmXHU1MzNhIiwibGF0aXR1ZGUiOiIzMC4yMTAwMDAiLCJsb25naXR1ZGUiOiIxMjAuMjExMDAwIiwiYXFpIjoiOTgiLCJ6cV9hcWkiOiIwIiwicG0yXzUiOiI3MyIsInBtMTAiOiIxMjEiLCJzbzIiOiI5Iiwibm8yIjoiOTYiLCJjbyI6IjEuMDAwIiwibzMiOiIxNCIsImNvbXBsZXhpbmRleCI6IjYuNzAxNzg1NyIsImxldmVsIjoiXHU0ZThjXHU3ZWE3IiwicXVhbGl0eSI6Ilx1ODI2ZiIsInByaW1hcnlfcG9sbHV0YW50IjoiUE0yLjUiLCJyYXRpbyI6MC4wMzE2MDAwMDAwMDAwMDAwMDMsImluZGV4cmF0aW8iOjAuMDIyM30seyJ0aW1lIjoiMjAyMC0wOS0xMCAwNzowMDowMCIsImNpdHluYW1lIjoiXHU2NzZkXHU1ZGRlIiwicG9pbnRnaWQiOiIyMjkiLCJwb2ludG5hbWUiOiJcdTU0OGNcdTc3NjZcdTVjMGZcdTViNjYiLCJwb2ludGxldmVsIjoiXHU1NmZkXHU2M2E3XHU3MGI5IiwicmVnaW9uIjoiXHU2MmYxXHU1ODg1XHU1MzNhIiwibGF0aXR1ZGUiOiIzMC4zMTE5MDAiLCJsb25naXR1ZGUiOiIxMjAuMTIwMDAwIiwiYXFpIjoiODkiLCJ6cV9hcWkiOiIwIiwicG0yXzUiOiI2NiIsInBtMTAiOiIxMjgiLCJzbzIiOiI2Iiwibm8yIjoiNTgiLCJjbyI6IjEuMTAwIiwibzMiOiI1NCIsImNvbXBsZXhpbmRleCI6IjUuODc2Nzg1NyIsImxldmVsIjoiXHU0ZThjXHU3ZWE3IiwicXVhbGl0eSI6Ilx1ODI2ZiIsInByaW1hcnlfcG9sbHV0YW50IjoiUE0xMCIsInJhdGlvIjowLjA0NzEwMDAwMDAwMDAwMDAwMywiaW5kZXhyYXRpbyI6MC4wNzA0MDAwMDAwMDAwMDAwMDR9LHsidGltZSI6IjIwMjAtMDktMTAgMDc6MDA6MDAiLCJjaXR5bmFtZSI6Ilx1Njc2ZFx1NWRkZSIsInBvaW50Z2lkIjoiMjI2IiwicG9pbnRuYW1lIjoiXHU1MzY3XHU5Zjk5XHU2ODY1IiwicG9pbnRsZXZlbCI6Ilx1NTZmZFx1NjNhN1x1NzBiOSIsInJlZ2lvbiI6Ilx1ODk3Zlx1NmU1Nlx1NTMzYSIsImxhdGl0dWRlIjoiMzAuMjQ1NjAwIiwibG9uZ2l0dWRlIjoiMTIwLjEyNzAwMCIsImFxaSI6Ijg3IiwienFfYXFpIjoiMCIsInBtMl81IjoiNjQiLCJwbTEwIjoiOTEiLCJzbzIiOiI1Iiwibm8yIjoiMzUiLCJjbyI6IjEuMDAwIiwibzMiOiIyOCIsImNvbXBsZXhpbmRleCI6IjQuNTExOTA0OCIsImxldmVsIjoiXHU0ZThjXHU3ZWE3IiwicXVhbGl0eSI6Ilx1ODI2ZiIsInByaW1hcnlfcG9sbHV0YW50IjoiUE0yLjUiLCJyYXRpbyI6MC4wODc0OTk5OTk5OTk5OTk5OTQsImluZGV4cmF0aW8iOjAuMDQ4MDk5OTk5OTk5OTk5OTk3fSx7InRpbWUiOiIyMDIwLTA5LTEwIDA3OjAwOjAwIiwiY2l0eW5hbWUiOiJcdTY3NmRcdTVkZGUiLCJwb2ludGdpZCI6IjIzMCIsInBvaW50bmFtZSI6Ilx1NGUzNFx1NWU3M1x1OTU0NyIsInBvaW50bGV2ZWwiOiJcdTU2ZmRcdTYzYTdcdTcwYjkiLCJyZWdpb24iOiJcdTRmNTlcdTY3NmRcdTUzM2EiLCJsYXRpdHVkZSI6IjMwLjQxODMwMCIsImxvbmdpdHVkZSI6IjEyMC4zMDEwMDAiLCJhcWkiOiI4NCIsInpxX2FxaSI6IjAiLCJwbTJfNSI6IjUxIiwicG0xMCI6IjExNyIsInNvMiI6IjUiLCJubzIiOiI3NCIsImNvIjoiMC44MDAiLCJvMyI6IjE5IiwiY29tcGxleGluZGV4IjoiNS4zODA2NTQ4IiwibGV2ZWwiOiJcdTRlOGNcdTdlYTciLCJxdWFsaXR5IjoiXHU4MjZmIiwicHJpbWFyeV9wb2xsdXRhbnQiOiJQTTEwIiwicmF0aW8iOjAuMTgzMTAwMDAwMDAwMDAwMDEsImluZGV4cmF0aW8iOjAuMTM0MDAwMDAwMDAwMDAwMDF9LHsidGltZSI6IjIwMjAtMDktMTAgMDc6MDA6MDAiLCJjaXR5bmFtZSI6Ilx1Njc2ZFx1NWRkZSIsInBvaW50Z2lkIjoiMjU0OSIsInBvaW50bmFtZSI6Ilx1Njg1MFx1NWU5MFx1NmM1Zlx1NTMxNyIsInBvaW50bGV2ZWwiOiJcdTc3MDFcdTYzYTdcdTcwYjkiLCJyZWdpb24iOiJcdTY4NTBcdTVlOTBcdTUzYmYiLCJsYXRpdHVkZSI6IjI5LjgwMzk2NiIsImxvbmdpdHVkZSI6IjExOS42NzExMTEiLCJhcWkiOiI4MiIsInpxX2FxaSI6IjAiLCJwbTJfNSI6IjYwIiwicG0xMCI6IjkxIiwic28yIjoiMjAiLCJubzIiOiIzNyIsImNvIjoiMC45MDAiLCJvMyI6IjUwIiwiY29tcGxleGluZGV4IjoiNC44MTAxMTkwIiwibGV2ZWwiOiJcdTRlOGNcdTdlYTciLCJxdWFsaXR5IjoiXHU4MjZmIiwicHJpbWFyeV9wb2xsdXRhbnQiOiJQTTIuNSIsInJhdGlvIjotMC4wMzUyOTk5OTk5OTk5OTk5OTgsImluZGV4cmF0aW8iOjAuMDQxMjAwMDAwMDAwMDAwMDAxfSx7InRpbWUiOiIyMDIwLTA5LTEwIDA3OjAwOjAwIiwiY2l0eW5hbWUiOiJcdTY3NmRcdTVkZGUiLCJwb2ludGdpZCI6IjIyMyIsInBvaW50bmFtZSI6Ilx1ODk3Zlx1NmVhYSIsInBvaW50bGV2ZWwiOiJcdTU2ZmRcdTYzYTdcdTcwYjkiLCJyZWdpb24iOiJcdTg5N2ZcdTZlNTZcdTUzM2EiLCJsYXRpdHVkZSI6IjMwLjI3NDcwMCIsImxvbmdpdHVkZSI6IjEyMC4wNjMwMDAiLCJhcWkiOiI4MCIsInpxX2FxaSI6IjAiLCJwbTJfNSI6IjU5IiwicG0xMCI6IjEwMCIsInNvMiI6IjUiLCJubzIiOiI2NCIsImNvIjoiMC44MDAiLCJvMyI6IjExIiwiY29tcGxleGluZGV4IjoiNS4wNjYzNjkwIiwibGV2ZWwiOiJcdTRlOGNcdTdlYTciLCJxdWFsaXR5IjoiXHU4MjZmIiwicHJpbWFyeV9wb2xsdXRhbnQiOiJQTTIuNSIsInJhdGlvIjowLjAyNTYwMDAwMDAwMDAwMDAwMSwiaW5kZXhyYXRpbyI6LTAuMDU3MjAwMDAwMDAwMDAwMDAxfSx7InRpbWUiOiIyMDIwLTA5LTEwIDA3OjAwOjAwIiwiY2l0eW5hbWUiOiJcdTY3NmRcdTVkZGUiLCJwb2ludGdpZCI6IjI1MzgiLCJwb2ludG5hbWUiOiJcdTY4NTBcdTVlOTBcdTZjNWZcdTUzNTciLCJwb2ludGxldmVsIjoiXHU3NzAxXHU2M2E3XHU3MGI5IiwicmVnaW9uIjoiXHU2ODUwXHU1ZTkwXHU1M2JmIiwibGF0aXR1ZGUiOiIyOS43OTYxMzYiLCJsb25naXR1ZGUiOiIxMTkuNjkwNTY4IiwiYXFpIjoiNzciLCJ6cV9hcWkiOiIwIiwicG0yXzUiOiI1NiIsInBtMTAiOiI5NiIsInNvMiI6IjExIiwibm8yIjoiMzMiLCJjbyI6IjAuNzAwIiwibzMiOiI1NiIsImNvbXBsZXhpbmRleCI6IjQuNTA0NzYxOSIsImxldmVsIjoiXHU0ZThjXHU3ZWE3IiwicXVhbGl0eSI6Ilx1ODI2ZiIsInByaW1hcnlfcG9sbHV0YW50IjoiUE0yLjUiLCJyYXRpbyI6MC4xMTU5LCJpbmRleHJhdGlvIjowLjAzOTgwMDAwMDAwMDAwMDAwMn0seyJ0aW1lIjoiMjAyMC0wOS0xMCAwNzowMDowMCIsImNpdHluYW1lIjoiXHU2NzZkXHU1ZGRlIiwicG9pbnRnaWQiOiIyMzIiLCJwb2ludG5hbWUiOiJcdTRlOTFcdTY4MTYiLCJwb2ludGxldmVsIjoiXHU1NmZkXHU2M2E3XHU3MGI5IiwicmVnaW9uIjoiXHU4OTdmXHU2ZTU2XHU1MzNhIiwibGF0aXR1ZGUiOiIzMC4xODA4MDAiLCJsb25naXR1ZGUiOiIxMjAuMDg4MDAwIiwiYXFpIjoiNzUiLCJ6cV9hcWkiOiIwIiwicG0yXzUiOiI1NSIsInBtMTAiOiI3OCIsInNvMiI6IjQiLCJubzIiOiI0NiIsImNvIjoiMC44MDAiLCJvMyI6IjIwIiwiY29tcGxleGluZGV4IjoiNC4yMjczODEwIiwibGV2ZWwiOiJcdTRlOGNcdTdlYTciLCJxdWFsaXR5IjoiXHU4MjZmIiwicHJpbWFyeV9wb2xsdXRhbnQiOiJQTTIuNSIsInJhdGlvIjowLjAxMzUsImluZGV4cmF0aW8iOjAuMDE4OX0seyJ0aW1lIjoiMjAyMC0wOS0xMCAwNzowMDowMCIsImNpdHluYW1lIjoiXHU2NzZkXHU1ZGRlIiwicG9pbnRnaWQiOiIyNDI3IiwicG9pbnRuYW1lIjoiXHU3NmQxXHU2ZDRiXHU2OTdjIiwicG9pbnRsZXZlbCI6Ilx1NzcwMVx1NjNhN1x1NzBiOSIsInJlZ2lvbiI6Ilx1NWVmYVx1NWZiN1x1NWUwMiIsImxhdGl0dWRlIjoiMjkuNDc0NDQyIiwibG9uZ2l0dWRlIjoiMTE5LjI3NjI0NyIsImFxaSI6IjUzIiwienFfYXFpIjoiMCIsInBtMl81IjoiMzUiLCJwbTEwIjoiNTUiLCJzbzIiOiI2Iiwibm8yIjoiNDIiLCJjbyI6IjAuNzAwIiwibzMiOiIxNSIsImNvbXBsZXhpbmRleCI6IjMuMjA0NDY0MyIsImxldmVsIjoiXHU0ZThjXHU3ZWE3IiwicXVhbGl0eSI6Ilx1ODI2ZiIsInByaW1hcnlfcG9sbHV0YW50IjoiUE0xMCIsInJhdGlvIjowLjAxOTE5OTk5OTk5OTk5OTk5OCwiaW5kZXhyYXRpbyI6MC4wODY1OTk5OTk5OTk5OTk5OTZ9LHsidGltZSI6IjIwMjAtMDktMTAgMDc6MDA6MDAiLCJjaXR5bmFtZSI6Ilx1Njc2ZFx1NWRkZSIsInBvaW50Z2lkIjoiMjI0IiwicG9pbnRuYW1lIjoiXHU1MzQzXHU1YzliXHU2ZTU2IiwicG9pbnRsZXZlbCI6Ilx1NTZmZFx1NjNhN1x1NzBiOSIsInJlZ2lvbiI6Ilx1NmRmM1x1NWI4OVx1NTNiZiIsImxhdGl0dWRlIjoiMjkuNjM1MDAwIiwibG9uZ2l0dWRlIjoiMTE5LjAyNjAwMCIsImFxaSI6IjUyIiwienFfYXFpIjoiMCIsInBtMl81IjoiMzEiLCJwbTEwIjoiNTMiLCJzbzIiOiI0Iiwibm8yIjoiMTQiLCJjbyI6IjAuNTAwIiwibzMiOiI4OCIsImNvbXBsZXhpbmRleCI6IjIuNzM0NTIzOCIsImxldmVsIjoiXHU0ZThjXHU3ZWE3IiwicXVhbGl0eSI6Ilx1ODI2ZiIsInByaW1hcnlfcG9sbHV0YW50IjoiUE0xMCIsInJhdGlvIjowLjAxOTU5OTk5OTk5OTk5OTk5OSwiaW5kZXhyYXRpbyI6MC4wNjc1OTk5OTk5OTk5OTk5OTN9LHsidGltZSI6IjIwMjAtMDktMTAgMDc6MDA6MDAiLCJjaXR5bmFtZSI6Ilx1Njc2ZFx1NWRkZSIsInBvaW50Z2lkIjoiMjQ0NyIsInBvaW50bmFtZSI6Ilx1N2IyY1x1NGU4Y1x1NGUyZFx1NWI2NiIsInBvaW50bGV2ZWwiOiJcdTc3MDFcdTYzYTdcdTcwYjkiLCJyZWdpb24iOiJcdTVlZmFcdTVmYjdcdTVlMDIiLCJsYXRpdHVkZSI6IjI5LjQ2MTI3MiIsImxvbmdpdHVkZSI6IjExOS4yODc2ODMiLCJhcWkiOiI1MiIsInpxX2FxaSI6IjAiLCJwbTJfNSI6IjM2IiwicG0xMCI6IjUzIiwic28yIjoiNCIsIm5vMiI6IjQzIiwiY28iOiIwLjcwMCIsIm8zIjoiMTIiLCJjb21wbGV4aW5kZXgiOiIzLjE3NzM4MTAiLCJsZXZlbCI6Ilx1NGU4Y1x1N2VhNyIsInF1YWxpdHkiOiJcdTgyNmYiLCJwcmltYXJ5X3BvbGx1dGFudCI6IlBNMTAiLCJyYXRpbyI6MC4wNjExOTk5OTk5OTk5OTk5OTcsImluZGV4cmF0aW8iOjAuMDA0NDk5OTk5OTk5OTk5OTk5N30seyJ0aW1lIjoiMjAyMC0wOS0xMCAwNzowMDowMCIsImNpdHluYW1lIjoiXHU2NzZkXHU1ZGRlIiwicG9pbnRnaWQiOiIyNTUzIiwicG9pbnRuYW1lIjoiXHU2ZGYzXHU1Yjg5XHU3M2FmXHU0ZmRkXHU1OTI3XHU2OTdjIiwicG9pbnRsZXZlbCI6Ilx1NzcwMVx1NjNhN1x1NzBiOSIsInJlZ2lvbiI6Ilx1NmRmM1x1NWI4OVx1NTNiZiIsImxhdGl0dWRlIjoiMjkuNTk2OTkwIiwibG9uZ2l0dWRlIjoiMTE5LjA1MzI3NSIsImFxaSI6IjUxIiwienFfYXFpIjoiMCIsInBtMl81IjoiMzAiLCJwbTEwIjoiNTIiLCJzbzIiOiI1Iiwibm8yIjoiMjkiLCJjbyI6IjAuNzAwIiwibzMiOiI1OSIsImNvbXBsZXhpbmRleCI6IjIuOTUyMDgzMyIsImxldmVsIjoiXHU0ZThjXHU3ZWE3IiwicXVhbGl0eSI6Ilx1ODI2ZiIsInByaW1hcnlfcG9sbHV0YW50IjoiUE0xMCIsInJhdGlvIjowLjEwODcsImluZGV4cmF0aW8iOjAuMTUwN31dLCJ0b3RhbCI6MTIsIndlYXRoZXIiOnsidGltZSI6IjIwMjAtMDktMTAgMDg6MDA6MDAiLCJ3ZWF0aGVyIjoiXHU1YzBmXHU5NmU4Iiwid2VhdGhlcl9pY29uIjoiaHR0cHM6XC9cL3d3dy56cTEyMzY5LmNvbVwvcmVzb3VyY2VcL2ltZ1wvd2VhdGhlcm5ld1wvMTEucG5nIiwidGVtcCI6IjI3IiwiaHVtaSI6IjY5IiwicmFpbiI6IjAiLCJ3ZCI6Ilx1NTM1N1x1OThjZSIsIndkYW5nbGUiOiIxODQiLCJ3cyI6IjIiLCJ3bCI6IjIiLCJ2aXNpYmlsaXR5IjoxMCwicHJlc3N1cmUiOiIxMDAyIiwidHEiOiJcdTk2MzRcdThmNmNcdTVjMGZcdTk2ZTgifX19fQ=="
    decrypt_str = _object.base64_decrypt_text(encrypt_str)
    print(f"base64解密: {decrypt_str}")
    # base64加密
    decrypt_str = "http://ggzy.xzsp.tj.gov.cn:80/jyxxcggg/948709.jhtml你好"
    encrypt_str = _object.base64_encrypt_text(decrypt_str)
    print(f"base64加密: {encrypt_str}")
    # md5加密
    decrypt_str = "http://ggzy.xzsp.tj.gov.cn:80/jyxxcggg/948709.jhtml你好"
    encrypt_str = _object.md5_encrypt_text(decrypt_str)
    print(f"md5加密: {encrypt_str}")
    # sha1加密
    decrypt_str = "http://ggzy.xzsp.tj.gov.cn:80/jyxxcggg/948709.jhtml你好"
    encrypt_str = _object.sha1_encrypt_text(decrypt_str)
    print(f"sha1加密: {encrypt_str}")
    # hmac加密
    decrypt_str = "http://ggzy.xzsp.tj.gov.cn:80/jyxxcggg/948709.jhtml你好"
    encrypt_str = _object.hmac_encrypt_text(decrypt_str, "auhuwie2")
    print(f"hamc加密: {encrypt_str}")


# pip3 uninstall pycrypto
# pip3 uninstall crypto
# pip3 install pycryptodome
# pip install pyDes
#
# 对称加密（加密解密密钥相同）：DES、DES3、AES
# 非对称加密（分公钥私钥）：RSA
# 信息摘要算法/签名算法：MD5、HMAC、SHA
# 前端实际使用中MD5、AES、RSA使用频率是最高的
# 几种加密方式配合次序：采用非对称加密算法管理对称算法的密钥，然后用对称加密算法加密数据，用签名算法生成非对称加密的摘要
# DES、DES3、AES、RSA、MD5、SHA、HMAC传入的消息或者密钥都是bytes数据类型，不是bytes数据类型的需要先转换；密钥一般是8的倍数
# Python实现RSA中，在rsa库中带有生成签名和校对签名的方法
# 安全性：DES<DES3=AES<RSA,至于MD5、SHA、HMAC不好说了
