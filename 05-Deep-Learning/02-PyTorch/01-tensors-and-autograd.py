# ======================================
# TOPIC: PYTORCH TENSORS AND AUTOGRAD
# LEVEL: INTERMEDIATE
# ID: deep-learning.pytorch.tensors-autograd
# ======================================

# INTRODUCTION
# PyTorch is the most used deep learning framework in research and industry,
# and most open LLMs are built with it. Its two superpowers: tensors that run
# on GPUs, and automatic differentiation.
#
# THEORY
# - A TENSOR is like a NumPy array, plus: device (cpu / cuda / mps) and
#   gradient tracking. torch.tensor, torch.zeros, torch.randn, torch.arange.
# - Most NumPy operations exist: +, *, @, sum, mean, reshape/view, indexing.
#   torch.from_numpy(a) and t.numpy() convert (sharing memory on CPU).
# - dtypes: float32 is the default for training; float16/bfloat16 save memory.
# - AUTOGRAD: create parameters with requires_grad=True. Operations record a
#   computational graph. loss.backward() computes d(loss)/d(param) for every
#   parameter into param.grad (the chain rule, automatically).
# - Gradients ACCUMULATE: zero them before each backward pass.
# - torch.no_grad() disables tracking (for evaluation / manual updates).
# - .detach() returns a tensor cut off from the graph.
#
# REAL-WORLD ANALOGY
# A self-recording calculator: every operation is written to a tape, and at
# the end you can play the tape backwards to get every derivative.
#
# SYNTAX:
#   w = torch.randn(3, requires_grad=True)
#   loss = ((x @ w - y) ** 2).mean(); loss.backward(); w.grad
#
# SMALL WORKING EXAMPLE:
import numpy as np
import torch

torch.manual_seed(0)
a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(a.shape, a.dtype, a.device)
print(a @ a, a.mean(dim=0), sep="\n")
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print("best available device:", device)
x = torch.tensor(2.0, requires_grad=True)
y = x ** 3 + 2 * x
y.backward()
print("dy/dx at 2 =", x.grad.item(), "(expected 3*4 + 2 = 14)")
X = torch.randn(100, 3)
true_w = torch.tensor([2.0, -1.0, 0.5])
targets = X @ true_w
w = torch.zeros(3, requires_grad=True)
for step in range(200):
    loss = ((X @ w - targets) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        w -= 0.1 * w.grad
    w.grad.zero_()
print("learned w:", w.detach().numpy().round(3), "final loss:", round(loss.item(), 6))
shared = torch.from_numpy(np.ones(3))
print("from numpy dtype:", shared.dtype)

# EXPLANATION (LINE BY LINE):
# torch.tensor(...)            -> float32 tensor on the CPU.
# a @ a, a.mean(dim=0)         -> same ideas as NumPy (dim instead of axis).
# device selection             -> GPU (cuda), Apple silicon (mps) or cpu.
# y = x^3 + 2x; y.backward()   -> autograd computes dy/dx = 3x^2 + 2 = 14.
# w = zeros(3, requires_grad=True) -> a trainable parameter.
# loss.backward()              -> fills w.grad.
# with torch.no_grad(): w -= ... -> update without recording the update itself.
# w.grad.zero_()               -> reset, otherwise gradients add up across steps.
# torch.from_numpy(np.ones(3)) -> float64 (NumPy's default) - convert to float32 for models.
#
# COMMON MISTAKES:
# 1. Forgetting to zero gradients (they accumulate).
# 2. Updating parameters outside torch.no_grad() (error or growing graph).
# 3. Mixing devices (tensor on mps + tensor on cpu -> error).
# 4. Feeding float64 NumPy data to float32 models.
# 5. Calling .numpy() on a tensor that requires grad (use .detach() first).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Create tensors with zeros, ones, randn and arange; reshape a 12-element
# tensor into 3x4 and 2x2x3; compute row sums and the max per column.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Use autograd to compute the gradient of f(a, b) = a^2 * b + sin(a * b) at
# (1.0, 2.0). Verify against the hand-derived formulas.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Fit logistic regression on make_classification data using only tensors and
# autograd (no nn.Module, no optimizer): implement sigmoid, BCE loss, the
# update loop and accuracy. Then show what goes wrong if you forget
# w.grad.zero_() (print gradient magnitudes over steps).

# YOUR CODE:

