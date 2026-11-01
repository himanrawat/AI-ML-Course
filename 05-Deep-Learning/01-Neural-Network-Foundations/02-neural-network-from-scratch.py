# ======================================
# TOPIC: A NEURAL NETWORK FROM SCRATCH (FORWARD PASS AND BACKPROPAGATION)
# LEVEL: ADVANCED
# ID: deep-learning.foundations.network-from-scratch
# ======================================

# INTRODUCTION
# Building a small network with only NumPy removes the magic: you will see
# exactly how forward passes, losses, gradients and updates fit together.
# (Maths: 02-Mathematics/02-Calculus/03-chain-rule and 04-gradient-descent.)
#
# THEORY
# Training loop for a 2-layer classifier:
#  1. FORWARD:  Z1 = X W1 + b1;  A1 = relu(Z1);  Z2 = A1 W2 + b2;  P = softmax(Z2)
#  2. LOSS:     cross-entropy = -mean(log P[correct class])
#  3. BACKWARD (chain rule, from the output back):
#       dZ2 = (P - Y_onehot) / n        (softmax + cross-entropy simplify nicely)
#       dW2 = A1.T dZ2;  db2 = sum(dZ2)
#       dA1 = dZ2 W2.T;  dZ1 = dA1 * (Z1 > 0)     (relu derivative)
#       dW1 = X.T dZ1;   db1 = sum(dZ1)
#  4. UPDATE:   W -= lr * dW for every parameter.
# - Initialise weights randomly with a small scale (He init for ReLU:
#   std = sqrt(2 / fan_in)); biases can start at 0.
# - An EPOCH is one pass over the training data.
#
# REAL-WORLD ANALOGY
# A relay team reviewing a lost race: the anchor runner's time is analysed
# first, then responsibility is passed back to each earlier runner in
# proportion to their contribution (backpropagation of blame).
#
# SYNTAX:
#   see the training loop below
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
X, y = make_moons(n_samples=600, noise=0.2, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
n_in, n_hidden, n_out = 2, 16, 2
W1 = rng.normal(0, np.sqrt(2 / n_in), (n_in, n_hidden)); b1 = np.zeros(n_hidden)
W2 = rng.normal(0, np.sqrt(2 / n_hidden), (n_hidden, n_out)); b2 = np.zeros(n_out)

def forward(X):
    Z1 = X @ W1 + b1
    A1 = np.maximum(0, Z1)
    Z2 = A1 @ W2 + b2
    Z2 = Z2 - Z2.max(axis=1, keepdims=True)
    P = np.exp(Z2) / np.exp(Z2).sum(axis=1, keepdims=True)
    return Z1, A1, P

lr = 0.5
Y = np.eye(n_out)[y_train]
for epoch in range(1, 501):
    Z1, A1, P = forward(X_train)
    loss = -np.mean(np.log(P[np.arange(len(y_train)), y_train] + 1e-12))
    dZ2 = (P - Y) / len(X_train)
    dW2, db2 = A1.T @ dZ2, dZ2.sum(axis=0)
    dZ1 = (dZ2 @ W2.T) * (Z1 > 0)
    dW1, db1 = X_train.T @ dZ1, dZ1.sum(axis=0)
    W1 -= lr * dW1; b1 -= lr * db1; W2 -= lr * dW2; b2 -= lr * db2
    if epoch in (1, 50, 200, 500):
        print(f"epoch {epoch:>3}: loss {loss:.4f}")
test_accuracy = np.mean(forward(X_test)[2].argmax(axis=1) == y_test)
print("test accuracy:", round(test_accuracy, 3))

# EXPLANATION (LINE BY LINE):
# make_moons                       -> non-linear 2-class data.
# He initialisation                -> random weights scaled for ReLU layers.
# forward()                        -> linear -> ReLU -> linear -> softmax
#                                     (max subtracted for numerical stability).
# Y = np.eye(n_out)[y_train]       -> one-hot targets.
# loss                             -> cross-entropy of the correct class probabilities.
# dZ2 = (P - Y) / n                -> gradient at the output scores.
# dW2, db2, dZ1, dW1, db1          -> chain rule backwards through each layer.
# W -= lr * dW                     -> gradient descent update for all 4 parameters.
# Loss falls and test accuracy reaches ~0.93: the network learned a curved boundary.
#
# COMMON MISTAKES:
# 1. Shape mismatches in the backward pass (check every dW has W's shape).
# 2. Forgetting the ReLU mask (Z1 > 0) in the backward pass.
# 3. Not dividing by n (learning rate effectively scales with batch size).
# 4. Initialising all weights to zero (hidden units stay identical).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add a check that prints the shape of every parameter and its gradient once,
# and assert they match. Then change n_hidden to 2, 4 and 64 and report test
# accuracy for each.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement gradient checking: for 5 random entries of W1 and W2, compare the
# analytic gradient with a numerical (central difference) gradient of the loss.
# Report the relative error (should be < 1e-6).

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Refactor the network into Layer classes (Linear, ReLU, SoftmaxCrossEntropy)
# each with forward() and backward(), and a Sequential container. Train a
# 3-layer network with mini-batches on the digits dataset (load_digits) and
# reach > 95% test accuracy.

# YOUR CODE:

