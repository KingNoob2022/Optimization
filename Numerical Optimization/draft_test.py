import tensorflow as tf
# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


x = tf.Variable(3.0)
print(x < 4.0)
if x < 4.0:
    print("Hello")

y = range(5)
print(y)