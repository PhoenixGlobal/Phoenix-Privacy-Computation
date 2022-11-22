#!/usr/bin/env python3

from web3 import Web3, HTTPProvider
import json
import asyncio
from log import log
import datetime,time
from millionaire import runJob


rpc = 'https://dataseed1.phoenix.global/rpc/'  # or http://39.104.61.131:6888
web3 = Web3(HTTPProvider(rpc))

abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"},{"indexed":false,"internalType":"string","name":"jobName","type":"string"},{"indexed":false,"internalType":"address","name":"partyA","type":"address"},{"indexed":false,"internalType":"address","name":"partyB","type":"address"},{"indexed":false,"internalType":"address","name":"partyC","type":"address"}],"name":"CreateAJob","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"DeleteAJob","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"}],"name":"MpcSubmit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"roundId","type":"uint256"}],"name":"StartAJob","type":"event"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"Jobs","outputs":[{"internalType":"uint256","name":"jobId","type":"uint256"},{"internalType":"string","name":"jobName","type":"string"},{"internalType":"uint256","name":"roundId","type":"uint256"},{"internalType":"address","name":"party0","type":"address"},{"internalType":"address","name":"party1","type":"address"},{"internalType":"address","name":"party2","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"ReSetRoundId","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"jobName","type":"string"},{"internalType":"address","name":"partyA","type":"address"},{"internalType":"address","name":"partyB","type":"address"},{"internalType":"address","name":"partyC","type":"address"}],"name":"createJob","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"deleteJob","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"getJobId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"getRoundId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"},{"internalType":"address","name":"part","type":"address"},{"internalType":"uint256","name":"roundId","type":"uint256"}],"name":"getSubmit","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"roundId","type":"uint256"}],"name":"getSubmitKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"},{"internalType":"uint256","name":"roundId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"mpcSubmit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"startJob","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
abi = json.loads(abi)

contractAddress = '0xDB7b9F5E999C99F410Db79e7e186384ce9882154'  # Your PrivacyComputation contract address

partyAddress = '0x383319a9363f82da8B7502fF35C8A7fAfd750dc9'    # Your party address
priKey='8659c8eee297288586c41860485bcf86a1fdf221a4bb95a9e3086e263634aee7'  # private key of party address

privacyContract = web3.eth.contract(address=contractAddress, abi=abi)

class PrivacyContract():
    def __init__(self):
        self.jobId=0
    def handle_event(self,event):
        eventStr = Web3.toJSON(event)
        print("event is ", eventStr)
        log(f"event is {eventStr}")

        dic = json.loads(eventStr)
        print("jobId is ",dic["args"]["jobId"])
        log(f'jobId is {dic["args"]["jobId"]}')
        self.jobId = dic["args"]["jobId"]
        runJob(self.jobId,self.submit)

    async def log_loop(self,event_filter, poll_interval):
        while True:
            for PairCreated in event_filter.get_new_entries():
                self.handle_event(PairCreated)
            await asyncio.sleep(poll_interval)

    def eventMonitor(self):
        event_filter = privacyContract.events.StartAJob.createFilter(fromBlock='latest')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    self.log_loop(event_filter, 5)))
        finally:
            loop.close()

    def submit(self,msg):
        roundId=privacyContract.functions.getRoundId(self.jobId).call()

        mybyte = str(msg).encode('utf-8')

        nonce=web3.eth.getTransactionCount(partyAddress)
        gasPrice=web3.eth.gasPrice

        transaction = privacyContract.functions.mpcSubmit(self.jobId,roundId, mybyte).buildTransaction({'gas':300000,"gasPrice": gasPrice, 'nonce':nonce })

        signed_txn = web3.eth.account.signTransaction(transaction, priKey)

        txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        msg=f"Transaction successful with hash: {txn_hash.hex()}"
        print(msg)
        log(msg)

pContract=PrivacyContract()
pContract.eventMonitor()