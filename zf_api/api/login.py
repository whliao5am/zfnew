# -*- coding: utf-8 -*-
import binascii
import rsa
import base64
import requests
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5


class Login(object):
    def __init__(self):
        self.main_url = 'http://jwc.xhu.edu.cn'
        self.key_url = 'http://jwc.xhu.edu.cn/xtgl/login_getPublicKey.html'
        self.login_url = 'http://jwc.xhu.edu.cn/xtgl/login_slogin.html'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Referer': self.login_url}
        self.sess = requests.Session()
        self.cookies = ''
        self.cookies_str = ''

    def login(self):
        """登陆"""
        req = self.sess.get(self.login_url, headers=self.headers)
        soup = BeautifulSoup(req.text, 'lxml')
        tokens = soup.find(id='csrftoken').get("value")

        res = self.sess.get(self.key_url, headers=self.headers).json()
        n = res['modulus']
        e = res['exponent']
        hmm = self.get_rsa('liao787960', n, e)

        login_data = {'csrftoken': tokens,
                      'yhm': '3120170807112',
                      'mm': hmm,
                      'mm': hmm}
        self.sess.post(self.login_url, headers=self.headers, data=login_data)
        self.cookies = self.sess.cookies
        self.cookies_str = '; '.join([item.name + '=' + item.value for item in self.cookies])

    @classmethod
    def encrypt_sqf(cls, pkey, str_in):
        """加载公钥"""
        private_key = pkey

        private_keybytes = base64.b64decode(private_key)
        prikey = RSA.importKey(private_keybytes)

        signer = PKCS1_v1_5.new(prikey)
        signature = base64.b64encode(signer.encrypt(str_in.encode("utf-8")))
        return signature

    @classmethod
    def get_rsa(cls, pwd, n, e):
        """对密码base64编码"""
        message = str(pwd).encode()
        rsa_n = binascii.b2a_hex(binascii.a2b_base64(n))
        rsa_e = binascii.b2a_hex(binascii.a2b_base64(e))
        key = rsa.PublicKey(int(rsa_n, 16), int(rsa_e, 16))
        encropy_pwd = rsa.encrypt(message, key)
        result = binascii.b2a_base64(encropy_pwd)
        return result

