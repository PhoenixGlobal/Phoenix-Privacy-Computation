import base64
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import requests
import json
from log import log

import os
dir_path = os.path.dirname(os.path.realpath(__file__))

priKeyFile=dir_path+"/myPrivateKey.pem"
apiUrl="http://localhost:8088/internal/"

def getKey(key_file):
    with open(key_file) as f:
        data = f.read()
        key = RSA.importKey(data)
    return key

def encryptData(pubKeyFile,msg):
    public_key = getKey(pubKeyFile)
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode("utf8"))))
    return encrypt_text.decode('utf-8')

def decryptData(encrypt_msg):
    private_key = getKey(priKeyFile)
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)
    return back_text.decode('utf-8')

def getAddressPri(address):
    res = requests.post(url=apiUrl+"queryAddress", data=json.dumps({'address': address}),
                        headers={'Content-Type': 'application/json'})
    print('getAddressPri res is :',res.text)
    log('getAddressPri res is :' + res.text)
    resDic = eval(res.text)
    if resDic["code"]!=200:
        priKey = ''
        print('getAddressPri priKey err,err msg is :', resDic["msg"])
        log('getAddressPri priKey err,err msg is :' + resDic["msg"])
        return priKey
    priMsg=resDic["addressInfo"]
    priKey=decryptData(priMsg)
    print('getAddressPri priKey is :',priKey)
    log('getAddressPri priKey is :'+priKey)
    return priKey

def getDatas(jobId,partyIndex):
    res = requests.post(url=apiUrl+"queryJobInputs", data=json.dumps({'jobID': jobId}),
                        headers={'Content-Type': 'application/json'})
    print('partyIndex is ',partyIndex,',getDatas res is :',res.text)
    log('partyIndex is '+str(partyIndex)+',getDatas res is :' + res.text)
    resDic = json.loads(res.text)

    if resDic["code"]!=200:
        data = ''
        print('getDatas data err,err msg is :', resDic["msg"])
        log('getDatas data err,err msg is :' + resDic["msg"])
        return data

    dataMsg=resDic["Inputs"][partyIndex]["data"]
    data=decryptData(dataMsg)
    print('partyIndex is ',partyIndex,',getDatas data is :',data)
    log('partyIndex is '+str(partyIndex)+',getDatas data is :'+data)
    return data