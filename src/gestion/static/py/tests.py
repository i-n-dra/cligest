import os
from aes import AES

"""
This is an exercise in secure symmetric-key encryption, implemented in pure
Python (no external libraries needed).

Original AES-128 implementation by Bo Zhu (http://about.bozhu.me) at 
https://github.com/bozhu/AES-Python . PKCS#7 padding, CBC mode, PKBDF2, HMAC,
byte array and string support added by me at https://github.com/boppreh/aes. 
Other block modes contributed by @righthandabacus.


Although this is an exercise, the `encrypt` and `decrypt` functions should
provide reasonable security to encrypted messages.
"""

class main:
    key = os.urandom(16)
    iv = os.urandom(16)
    text = 'hola...á¿?' # funciona con caracteres en español
    text = text.encode('utf-8')
    encrypted = AES(key).encrypt_cbc(text, iv)
    print(f'encrypted: {encrypted}\ndecrypted: {AES(key).decrypt_cbc(encrypted, iv)}\ndecrypted str: {AES(key).decrypt_cbc(encrypted, iv).decode('utf-8')}')

def run():
    main()

if __name__ == '__main__':
    run()
