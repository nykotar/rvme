import random
import base64
from cryptography.fernet import Fernet

from django.conf import settings

def gen_tid():
    tid = list()
    for _ in range(8):
        tid.append(str(random.randint(0, 9)))
    tid.insert(4, '-')
    return ''.join(tid)

def encrypt(text):
    fernet = Fernet(settings.FERNET_KEY)
    enc_text = fernet.encrypt(text.encode('utf-8'))
    enc_text = base64.urlsafe_b64encode(enc_text).decode('ascii')
    return enc_text

def decrypt(string):
    fernet = Fernet(settings.FERNET_KEY)
    dec_text = base64.urlsafe_b64decode(string.encode('ascii'))
    dec_text = fernet.decrypt(dec_text).decode('utf-8')
    return dec_text