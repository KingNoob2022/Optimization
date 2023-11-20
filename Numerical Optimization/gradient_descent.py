import tensorflow as tf
# Just disables the warning, doesn't take advantage of AVX/FMA to run faster
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

x1 = tf.Variable(0.)
x2 = tf.Variable(0.)
x3 = tf.Variable(0.)
nuy = 0.5
c = 0.6


def objective_func(x1, x2, x3):
  return x1 ** 2 + x2 ** 2 + x3 ** 2 - x1 * x2 - x2 * x3 + x1 + x3


num_epochs = 100
for i in range(num_epochs):
    with tf.GradientTape() as tape:
      tape.watch([x1, x2, x3])
      y = objective_func(x1, x2, x3)
    grad = tape.gradient(y, [x1, x2, x3])

    alpha = 1
    descent = tf.norm(grad) ** 2
    while objective_func(x1 - alpha * grad[0], x2 - alpha * grad[1], x3 - alpha * grad[2]) > objective_func(x1, x2, x3) - \
            c * alpha * descent:
        alpha = alpha * nuy
    x1, x2, x3 = (x1 - alpha * grad[0], x2 - alpha * grad[1], x3 - alpha * grad[2])

print(x1, x2, x3)