# ======================================
# TOPIC: OPTIMIZERS AND REGULARIZATION IN DEEP LEARNING
# LEVEL: ADVANCED
# ID: deep-learning.pytorch.optimizers-regularization
# ======================================

# INTRODUCTION
# Big networks easily memorise their training data, and training can be slow
# or unstable. Optimizers and regularization techniques make training fast,
# stable and generalisable.
#
# THEORY
# OPTIMIZERS:
# - SGD: w -= lr * grad. With MOMENTUM: keep a running direction (velocity).
# - ADAM: per-parameter adaptive step sizes from running averages of the
#   gradient and its square. AdamW = Adam with decoupled weight decay
#   (the standard for transformers).
# - LEARNING-RATE SCHEDULES: warm-up then decay (cosine, step) are standard.
# - GRADIENT CLIPPING (clip_grad_norm_) prevents exploding updates.
# REGULARIZATION:
# - WEIGHT DECAY (L2): pulls weights toward zero.
# - DROPOUT: randomly zero activations during training (p = 0.1-0.5), so the
#   network cannot rely on single units; disabled in eval mode.
# - NORMALIZATION layers (BatchNorm, LayerNorm) stabilise training.
# - EARLY STOPPING and DATA AUGMENTATION.
#
# REAL-WORLD ANALOGY
# Momentum is a ball rolling downhill that keeps its speed through small
# bumps. Dropout is a football team practising with random players benched,
# so nobody becomes a single point of failure.
#
# SYNTAX:
#   torch.optim.AdamW(params, lr=1e-3, weight_decay=0.01)
#   nn.Dropout(p=0.3); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
#
# SMALL WORKING EXAMPLE:
import torch
from torch import nn

torch.manual_seed(0)
X = torch.randn(80, 20)
y = (X[:, 0] + 0.5 * X[:, 1] > 0).long()
y_noisy = y.clone(); y_noisy[:12] = 1 - y_noisy[:12]
X_val = torch.randn(1000, 20)
y_val = (X_val[:, 0] + 0.5 * X_val[:, 1] > 0).long()

def make_model(dropout):
    return nn.Sequential(nn.Linear(20, 256), nn.ReLU(), nn.Dropout(dropout),
                         nn.Linear(256, 256), nn.ReLU(), nn.Dropout(dropout), nn.Linear(256, 2))

def run(optimizer_name, dropout=0.0, weight_decay=0.0, epochs=300):
    torch.manual_seed(1)
    model = make_model(dropout)
    if optimizer_name == "sgd":
        opt = torch.optim.SGD(model.parameters(), lr=0.01, weight_decay=weight_decay)
    else:
        opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=weight_decay)
    loss_fn = nn.CrossEntropyLoss()
    for _ in range(epochs):
        model.train()
        opt.zero_grad()
        loss = loss_fn(model(X), y_noisy)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
    model.eval()
    with torch.no_grad():
        train_acc = (model(X).argmax(1) == y_noisy).float().mean().item()
        val_acc = (model(X_val).argmax(1) == y_val).float().mean().item()
    return train_acc, val_acc

for label, kwargs in [("SGD", dict(optimizer_name="sgd")),
                      ("AdamW", dict(optimizer_name="adamw")),
                      ("AdamW + dropout + decay", dict(optimizer_name="adamw", dropout=0.5, weight_decay=0.1))]:
    train_acc, val_acc = run(**kwargs)
    print(f"{label:<26} train {train_acc:.2f} | validation {val_acc:.2f}")
layer = nn.Dropout(0.5)
ones = torch.ones(8)
print("dropout train:", layer.train()(ones).tolist())
print("dropout eval: ", layer.eval()(ones).tolist())

# EXPLANATION (LINE BY LINE):
# 80 training samples, 20 features, 12 labels deliberately flipped (noise).
# A big network (256-256) can memorise the noisy labels.
# SGD with a small lr learns slowly within 300 steps.
# AdamW converges fast and memorises the noise (train ~1.0, lower validation).
# Dropout + weight decay give only a small validation gain here (~0.69 -> ~0.71):
#   with just 80 noisy samples, regularization cannot replace missing data.
#   Question 1 asks you to measure how the trade-off changes.
# clip_grad_norm_                 -> caps the gradient's overall size each step.
# nn.Dropout in train mode        -> zeroes ~half the values and scales the rest x2;
#                                    in eval mode it does nothing.
#
# COMMON MISTAKES:
# 1. Evaluating in train mode (dropout still active -> noisy, lower accuracy).
# 2. Using Adam's weight_decay expecting AdamW behaviour.
# 3. A learning rate that is fine for Adam (1e-3) being far too small for SGD.
# 4. Adding every regularizer at once without measuring each.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Using run(), compare dropout = 0.0, 0.2, 0.5, 0.8 with AdamW. Report train
# and validation accuracy and pick the best value.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Implement SGD with momentum yourself (velocity = beta * velocity + grad;
# w -= lr * velocity) for a 2D quadratic bowl with very different curvatures,
# and plot the paths of plain SGD vs momentum on a contour plot.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Implement a warm-up + cosine-decay learning-rate schedule with
# torch.optim.lr_scheduler.LambdaLR, plot the learning rate over 1,000 steps,
# and train the digits classifier with it vs a constant learning rate.
# Compare loss curves.

# YOUR CODE:

