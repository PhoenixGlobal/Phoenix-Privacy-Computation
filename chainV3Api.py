#!/usr/bin/env python3
import time

from web3 import Web3, HTTPProvider
import json
import asyncio
from log import log
import subprocess
import os

rpc = 'https://dataseed1.phoenix.global/rpc/'  # or http://39.104.61.131:6888
web3 = Web3(HTTPProvider(rpc))

abi='[{"inputs":[{"internalType":"address","name":"ccd","type":"address"},{"internalType":"address","name":"ccdCollectorAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"},{"indexed":false,"internalType":"string","name":"jobName","type":"string"},{"indexed":false,"internalType":"address","name":"partyA","type":"address"},{"indexed":false,"internalType":"address","name":"partyB","type":"address"},{"indexed":false,"internalType":"address","name":"partyC","type":"address"}],"name":"CreateAJob","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"DeleteAJob","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"roundId","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"},{"indexed":false,"internalType":"uint256","name":"ccdCost","type":"uint256"}],"name":"MpcSubmit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"roundId","type":"uint256"}],"name":"StartAJob","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"jobId","type":"uint256"},{"indexed":false,"internalType":"string","name":"jobName","type":"string"},{"indexed":false,"internalType":"address","name":"partyA","type":"address"},{"indexed":false,"internalType":"address","name":"partyB","type":"address"},{"indexed":false,"internalType":"address","name":"partyC","type":"address"}],"name":"UpdateAJob","type":"event"},{"inputs":[],"name":"Ccd","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"Jobs","outputs":[{"internalType":"uint256","name":"jobId","type":"uint256"},{"internalType":"string","name":"jobName","type":"string"},{"internalType":"uint256","name":"roundId","type":"uint256"},{"internalType":"address","name":"party0","type":"address"},{"internalType":"address","name":"party1","type":"address"},{"internalType":"address","name":"party2","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"ReSetRoundId","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"ccdCollector","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"jobName","type":"string"},{"internalType":"address","name":"partyA","type":"address"},{"internalType":"address","name":"partyB","type":"address"},{"internalType":"address","name":"partyC","type":"address"}],"name":"createJob","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"deleteJob","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"getJobId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"getRoundId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"},{"internalType":"address","name":"part","type":"address"},{"internalType":"uint256","name":"roundId","type":"uint256"}],"name":"getSubmit","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint256","name":"roundId","type":"uint256"}],"name":"getSubmitKey","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"},{"internalType":"uint256","name":"roundId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"uint256","name":"ccdCost","type":"uint256"}],"name":"mpcSubmit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"ccdAddress","type":"address"}],"name":"setCcd","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"ccdCollectorAddress","type":"address"}],"name":"setCcdCollector","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"}],"name":"startJob","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"jobId","type":"uint256"},{"internalType":"address","name":"partyA","type":"address"},{"internalType":"address","name":"partyB","type":"address"},{"internalType":"address","name":"partyC","type":"address"}],"name":"updateJob","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
abi = json.loads(abi)

contractAddress = '0x0efE68F95e6808896AF379bbfdaF5945385Eef94'  # Your PrivacyComputation contract address

privacyContract = web3.eth.contract(address=contractAddress, abi=abi)

currentCat = os.getcwd()

class PrivacyContract():
    def __init__(self):
        self.jobIdsWaitForStart=[]
    def handle_event(self,event):
        eventStr = Web3.toJSON(event)
        print("event is ", eventStr)
        log(f"event is {eventStr}")

        dic = json.loads(eventStr)
        jobId = dic["args"]["jobId"]

        print("jobId is ",jobId)
        log(f'jobId is {jobId}')
        jobId=str(jobId)
        self.jobIdsWaitForStart.append(jobId)


    async def log_loop(self,event_filter, poll_interval):
        while True:
            for PairCreated in event_filter.get_new_entries():
                self.handle_event(PairCreated)
            await asyncio.sleep(poll_interval)

    def eventMonitor(self):
        print("Begin start eventMonitor")
        log("Begin start eventMonitor")
        event_filter = privacyContract.events.StartAJob.createFilter(fromBlock='latest')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    self.log_loop(event_filter, 5)))
        finally:
            loop.close()

    def runJobsLoop(self, poll_interval):
        print("Begin start runJobsLoop")
        log("Begin start runJobsLoop")
        while True:
            if len(self.jobIdsWaitForStart)>0:
                jobId=self.jobIdsWaitForStart[0]
                self.startJobId(jobId)
                # del self.jobIdsWaitForStart[0]
                self.jobIdsWaitForStart.remove(jobId)
            time.sleep(poll_interval)


    def startJobId(self, jobId):
        print("Begin startJobId,jobId is ", jobId)
        log(f'Begin startJobId, jobId is {jobId}')
        os.chdir(currentCat + "/millionaire0")
        p0 = subprocess.Popen(["python3", "matrixComputationV2.py", "--party_id=0", jobId])
        print("P0 start job,jobId is ", jobId)
        log(f'P0 start job,jobId is {jobId}')
        os.chdir(currentCat + "/millionaire1")
        p1 = subprocess.Popen(["python3", "matrixComputationV2.py", "--party_id=1", jobId])
        print("P1 start job,jobId is ", jobId)
        log(f'P1 start job,jobId is {jobId}')
        os.chdir(currentCat + "/millionaire2")
        p2 = subprocess.Popen(["python3", "matrixComputationV2.py", "--party_id=2", jobId])
        print("P2 start job,jobId is ", jobId)
        log(f'P2 start job,jobId is {jobId}')
        p0.wait(timeout=15)
        print("P0 end job,jobId is ", jobId)
        log(f'P0 end job,jobId is {jobId}')
        p1.wait(timeout=15)
        print("P1 end job,jobId is ", jobId)
        log(f'P1 end job,jobId is {jobId}')
        p2.wait(timeout=15)
        print("P2 end job,jobId is ", jobId)
        log(f'P2 end job,jobId is {jobId}')
        print("End startJobId,jobId is ", jobId)
        log(f'End startJobId, jobId is {jobId}')

# pContract=PrivacyContract()
# pContract.eventMonitor()
# pContract.runJobsLoop()

