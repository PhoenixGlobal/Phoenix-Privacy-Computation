#!/usr/bin/env python3

# import rosetta package
import latticex.rosetta as rtt
import tensorflow as tf
from log import log
import random
import datetime,time

# activate protocol, here use SecureNN.
rtt.activate("SecureNN")

sess=tf.Session()

def runJob(jobId,submit):
    print("Begin runJob,JobId is ", jobId, ",now time is ", datetime.datetime.now())
    log(f"Begin runJob,JobId is {jobId},now time is {datetime.datetime.now()}")
    # get private data from console
    Alice = tf.Variable(rtt.private_console_input(0))
    Bob = tf.Variable(rtt.private_console_input(1))

    # define comparsion operation
    res = tf.greater(Alice, Bob)

    # run computation

    sess.run(tf.global_variables_initializer())
    res = sess.run(res)

    # get the result and output
    result=sess.run(rtt.SecureReveal(res))
    print('ret:', result)  # ret: 1.0
    log('ret:'+str(result))

    submit(result)
    print("End runJob,JobId is ", jobId, ",now time is ", datetime.datetime.now())
    log(f"End runJob,JobId is {jobId},now time is {datetime.datetime.now()}")
    print("---------------------------------------------")


