#!/usr/bin/env python3

# import rosetta package
import latticex.rosetta as rtt
import tensorflow as tf
from chain import submit
from log import log

# activate protocol, here use SecureNN.
rtt.activate("SecureNN")

# get private data from console
Alice = tf.Variable(rtt.private_console_input(0))
Bob = tf.Variable(rtt.private_console_input(1))

# define comparsion operation
res = tf.greater(Alice, Bob)

# run computation
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    res = sess.run(res)

    # get the result and output
    result=sess.run(rtt.SecureReveal(res))
    print('ret:', result)  # ret: 1.0
    log('ret:'+str(result))

submit(result)


