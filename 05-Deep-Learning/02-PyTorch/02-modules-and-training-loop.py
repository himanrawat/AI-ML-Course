# ======================================
# TOPIC: NN.MODULE, DATALOADERS AND THE TRAINING LOOP
# LEVEL: INTERMEDIATE
# ID: deep-learning.pytorch.training-loop
# ======================================

# INTRODUCTION
# Every PyTorch project - from MNIST to fine-tuning an LLM - follows the same
# training loop. Learn it once, use it everywhere.
#
# THEORY
# - nn.Module: subclass it, define layers in __init__, computation in forward().
#   nn.Linear, nn.ReLU, nn.Dropout, nn.Sequential, model.parameters().
# - Dataset (__len__, __getitem__) + DataLoader(batch_size, shuffle) produce
#   mini-batches.
# - Loss functions: nn.CrossEntropyLoss (takes raw LOGITS + class indices;
#   it applies softmax internally), nn.MSELoss, nn.BCEWithLogitsLoss.
# - Optimizers: torch.optim.SGD, Adam/AdamW (lr ~1e-3 is a common start).
# - The loop, per batch:
#     optimizer.zero_grad(); logits = model(xb); loss = loss_fn(logits, yb)
#     loss.backward(); optimizer.step()
# - model.train() vs model.eval(): changes dropout/batch-norm behaviour.
#   Evaluate under torch.no_grad().
# - Save weights: torch.save(model.state_dict(), path); load with
#   model.load_state_dict(torch.load(path)).
#
# REAL-WORLD ANALOGY
# A gym routine: each set (batch) you lift (forward), check your form (loss),
# get feedback (backward) and adjust (step); after each week (epoch) you test
# your strength (evaluation).
#
# SYNTAX:
#   for xb, yb in loader:
#       optimizer.zero_grad(); loss = loss_fn(model(xb), yb); loss.backward(); optimizer.step()
#
# SMALL WORKING EXAMPLE:
import torch
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(0)
X, y = load_digits(return_X_y=True)
X = X / 16.0
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
to_tensor = lambda a, dtype: torch.tensor(a, dtype=dtype)
train_ds = TensorDataset(to_tensor(X_train, torch.float32), to_tensor(y_train, torch.long))
test_ds = TensorDataset(to_tensor(X_test, torch.float32), to_tensor(y_test, torch.long))
train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
test_loader = DataLoader(test_ds, batch_size=256)

class DigitClassifier(nn.Module):
    def __init__(self, n_in=64, n_hidden=128, n_classes=10):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_classes))

    def forward(self, x):
        return self.net(x)

def evaluate(model, loader):
    model.eval()
    correct = 0
    with torch.no_grad():
        for xb, yb in loader:
            correct += (model(xb).argmax(dim=1) == yb).sum().item()
    return correct / len(loader.dataset)

model = DigitClassifier()
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
print("parameters:", sum(p.numel() for p in model.parameters()))
for epoch in range(1, 11):
    model.train()
    total = 0.0
    for xb, yb in train_loader:
        optimizer.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        optimizer.step()
        total += loss.item() * len(xb)
    if epoch % 3 == 1 or epoch == 10:
        print(f"epoch {epoch:>2}: train loss {total / len(train_ds):.4f} | test acc {evaluate(model, test_loader):.3f}")

# EXPLANATION (LINE BY LINE):
# X / 16.0                     -> scale pixel values (0..16) to 0..1.
# TensorDataset + DataLoader   -> shuffled mini-batches of 64.
# class DigitClassifier(nn.Module) -> layers in __init__, computation in forward.
# evaluate()                   -> eval mode + no_grad; accuracy over the test set.
# CrossEntropyLoss             -> expects raw logits (no softmax in the model).
# Adam(model.parameters(), lr=1e-3) -> the optimizer updates every parameter.
# The 4-line core: zero_grad, forward+loss, backward, step.
# loss.item() * len(xb)        -> accumulate a per-sample average loss.
#
# COMMON MISTAKES:
# 1. Adding softmax before CrossEntropyLoss.
# 2. Forgetting model.eval() / torch.no_grad() during evaluation.
# 3. Class labels as float instead of long for CrossEntropyLoss.
# 4. Not shuffling the training loader.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Change the hidden size to 32 and 512 and the learning rate to 1e-2 and 1e-4.
# Record the final test accuracy for each run in a small table (comments).

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Write a custom Dataset class for the digits data that applies a random
# horizontal shift augmentation (np.roll on the 8x8 image) during training.
# Add a validation split, save the best model's state_dict when validation
# accuracy improves, and reload it at the end.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a reusable fit(model, train_loader, val_loader, epochs, optimizer,
# loss_fn, device, patience) function with early stopping, a history dict, a
# learning-rate scheduler (torch.optim.lr_scheduler.ReduceLROnPlateau) and
# support for running on mps/cuda when available. Use it on the digits data.

# YOUR CODE:

