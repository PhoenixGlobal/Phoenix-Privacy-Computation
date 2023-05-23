#!/usr/bin/env python3

# import rosetta package
import latticex.rosetta as rtt
import tensorflow as tf
from log import log
import datetime
import os


import sys
from addressApi import getAddressPri,getDatas
from chainV3Api import *
from reversePolishNotation import MatrixCombinationComputation

theJobId=int(sys.argv[2])
print('The JobId gotten from sys.argv is ',theJobId)
log(f"The JobId gotten from sys.argv is  {theJobId}")

# activate protocol, here use SecureNN.
rtt.activate("SecureNN")

def stats_graph(graph):
    flops = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.float_operation())
    params = tf.profiler.profile(graph, options=tf.profiler.ProfileOptionBuilder.trainable_variables_parameter())
    print('FLOPs: {};    Trainable params: {}'.format(flops.total_float_ops, params.total_parameters))
    log(f"FLOPs: {flops.total_float_ops};    Trainable params: {params.total_parameters}")
    return params.total_parameters

def runJob(jobId, data_a,data_b,data_c):
    print("Begin runJob,JobId is ", jobId, ",now time is ", datetime.datetime.now())
    log(f"Begin runJob,JobId is {jobId},now time is {datetime.datetime.now()}")

    sess = tf.Session()
    graph = sess.graph

    # get private data from every party
    a = eval(data_a)
    matrix_a = tf.Variable(rtt.private_input(0, a))
    b = eval(data_b)
    matrix_b = tf.Variable(rtt.private_input(1, b))
    c = eval(data_c)
    print('input c is :', c)
    log('input c is :' + str(c))
    matrix_c = tf.Variable(rtt.private_input(2, c))

    # use the matrix combination operation.
    expression=getExpression(jobId)
    print('expression is ', expression)
    log(f"expression is {expression}")
    res = MatrixCombinationComputation(expression,matrix_a,matrix_b,matrix_c)

    total_parameters = stats_graph(graph)
    cost = total_parameters * 10**15
    print('total_parameters is ', total_parameters)
    log(f"total_parameters is {total_parameters}")

    # run computation

    sess.run(tf.global_variables_initializer())
    res = sess.run(res)
    print('local ciphertext result:', res)
    log('local ciphertext result:' + str(res))

    # get the result and output
    a_b_c_can_get_plain = 0b111
    result=sess.run(rtt.SecureReveal(res,a_b_c_can_get_plain))
    print('plaintext matmul result:', result)  # ret: 1.0
    log('plaintext matmul result:'+str(result))

    submit(result,jobId,cost)
    print("End runJob,JobId is ", jobId, ",now time is ", datetime.datetime.now())
    log(f"End runJob,JobId is {jobId},now time is {datetime.datetime.now()}")
    print("---------------------------------------------")
    return total_parameters

def getExpression(jobId):
    expression = privacyContract.functions.getExpression(jobId).call()
    return expression

def submit(msg,jobId, ccdCost):
    job=privacyContract.functions.Jobs(jobId).call()
    partyAddress=job[6]
    priKey=getAddressPri(partyAddress)
    if priKey=='':
        print('P2 getAddressPri priKey is empty,return')
        log("P2 getAddressPri priKey is empty,return")
        sys.exit()
    roundId=privacyContract.functions.getRoundId(jobId).call()

    mybyte = str(msg).encode('utf-8')

    nonce=web3.eth.getTransactionCount(partyAddress)
    gasPrice=web3.eth.gasPrice

    transaction = privacyContract.functions.mpcSubmit(jobId,roundId, mybyte,ccdCost).buildTransaction({'gas':3000000,"gasPrice": gasPrice, 'nonce':nonce })

    signed_txn = web3.eth.account.signTransaction(transaction, priKey)

    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    msg=f"Transaction successful with hash: {txn_hash.hex()}"
    print(msg)
    log(msg)

dataA=getDatas(str(theJobId),0)
if dataA == '':
    print('P2 getDatas dataA is empty,return')
    log("P2 getDatas dataA is empty,return")
    sys.exit()
dataB=getDatas(str(theJobId),1)
if dataB == '':
    print('P2 getDatas dataB is empty,return')
    log("P2 getDatas dataB is empty,return")
    sys.exit()
dataC=getDatas(str(theJobId),2)
if dataC == '':
    print('P2 getDatas dataC is empty,return')
    log("P2 getDatas dataC is empty,return")
    sys.exit()
runJob(theJobId,dataA,dataB,dataC)