from web3 import Web3, HTTPProvider
import json
from log import log

rpc = 'https://dataseed1.phoenix.global/rpc/'  # or http://39.104.61.131:6888
web3 = Web3(HTTPProvider(rpc))

abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"ReSetRoundId","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"RoundId","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"roundId","type":"uint32"},{"internalType":"address","name":"part","type":"address"}],"name":"getResult","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRoundId","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"roundId","type":"uint32"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mpcSubmit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"party0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"party1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"party2","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"","type":"uint32"}],"name":"results","outputs":[{"internalType":"bool","name":"isValue","type":"bool"},{"internalType":"int8","name":"length","type":"int8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"partyA","type":"address"},{"internalType":"address","name":"partyB","type":"address"},{"internalType":"address","name":"partyC","type":"address"}],"name":"setPartyAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
abi = json.loads(abi)

contractAddress = '0xD77ADa9D8311ec6B60a427608803C8b7B339F6f7'  # Your PrivacyComputation contract address

partyAddress = '0x383319a9363f82da8B7502fF35C8A7fAfd750dc9'    # Your party address
priKey='8659c8eee297288586c41860485bcf86a1fdf221a4bb95a9e3086e263634aee7'  # private key of party address

privacyContract = web3.eth.contract(address=contractAddress, abi=abi)

def submit(msg):
    roundId=privacyContract.functions.getRoundId().call()

    mybyte = str(msg).encode('utf-8')

    nonce=web3.eth.getTransactionCount(partyAddress)
    gasPrice=web3.eth.gasPrice

    transaction = privacyContract.functions.mpcSubmit(roundId, mybyte).buildTransaction({'gas':300000,"gasPrice": gasPrice, 'nonce':nonce })

    signed_txn = web3.eth.account.signTransaction(transaction, priKey)

    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    msg=f"Transaction successful with hash: {txn_hash.hex()}"
    print(msg)
    log(msg)
