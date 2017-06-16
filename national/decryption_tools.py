import urllib2
import urllib
import json
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def get_encrypted_votes(url):
    full_url = url + '/get_votes/'
    request = urllib2.Request(full_url)
    response = urllib2.urlopen(request)

    return json.loads(response.read())

def decrypt_vote(encrypted_vote, key):
    cipher_text = base64.b64decode(encrypted_vote['vote'])
    key = key.replace('\\n', '\n')
    rsa_key = RSA.importKey(key)
    cipher = PKCS1_OAEP.new(rsa_key)
    vote_json = cipher.decrypt(cipher_text)
    return json.loads(vote_json)
