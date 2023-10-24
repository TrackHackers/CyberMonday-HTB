import os
import json
import hashlib
import sys
import hmac
import base64
import string
import requests
from Crypto.Cipher import AES
from phpserialize import loads, dumps

#https://gist.github.com/bluetechy/5580fab27510906711a2775f3c4f5ce3

def mcrypt_decrypt(value, iv):
    global key
    AES.key_size = [len(key)]
    crypt_object = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    return crypt_object.decrypt(value)


def mcrypt_encrypt(value, iv):
    global key
    AES.key_size = [len(key)]
    crypt_object = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    return crypt_object.encrypt(value)


def decrypt(bstring):
    global key
    dic = json.loads(base64.b64decode(bstring).decode())
    mac = dic['mac']
    value = bytes(dic['value'], 'utf-8')
    iv = bytes(dic['iv'], 'utf-8')
    if mac == hmac.new(key, iv+value, hashlib.sha256).hexdigest():
        return mcrypt_decrypt(base64.b64decode(value), base64.b64decode(iv))
        #return loads(mcrypt_decrypt(base64.b64decode(value), base64.b64decode(iv))).decode()
    return ''


def encrypt(string):
    global key
    iv = os.urandom(16)
    #string = dumps(string)
    padding = 16 - len(string) % 16
    string += bytes(chr(padding) * padding, 'utf-8')
    value = base64.b64encode(mcrypt_encrypt(string, iv))
    iv = base64.b64encode(iv)
    mac = hmac.new(key, iv+value, hashlib.sha256).hexdigest()
    dic = {'iv': iv.decode(), 'value': value.decode(), 'mac': mac}
    return base64.b64encode(bytes(json.dumps(dic), 'utf-8'))

app_key ='EX3zUxJkzEAY2xM4pbOfYMJus+bjx6V25Wnas+rFMzA='
key = base64.b64decode(app_key)
decrypted_cookie = decrypt('eyJpdiI6IitEVjZkSGExSVkvdFlRYXUrR0NxNEE9PSIsInZhbHVlIjoib09SdXprMURvOVpFaElLdXdvbW1oQWo4MUVnYTRURy93TitlZ00ydGY3UW1KSHNyT1g1ZStwYkVPUnJFUVVWSjU3YWU3VEtkM3BQVjBUNlk0TENnaFh3M0Evb09TTVRwTHNYRDBoSythb3poUDFlWmZLL3lKYWtraDRUeEhTVUYiLCJtYWMiOiI5ODQwZWUyZTcyYzU3ZmY1NmZjNjA3ZDYwMWIyYTI2MmNiZDBlMDg2MDZmYWFiNjY2ZDdhOTRlZWI3MTQyNThjIiwidGFnIjoiIn0')
print(decrypted_cookie)
