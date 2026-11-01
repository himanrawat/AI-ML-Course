# ======================================
# TOPIC: CONVOLUTIONAL NEURAL NETWORKS (CNNS)
# LEVEL: ADVANCED
# ID: deep-learning.architectures.cnn
# ======================================

# INTRODUCTION
# Images have structure: nearby pixels belong together, and a cat is a cat
# wherever it appears. CNNs exploit this and power image classification,
# detection and the vision encoders of multimodal models.
#
# THEORY
# - A CONVOLUTION slides a small filter (kernel, e.g. 3x3) over the image,
#   computing a dot product at each position -> a FEATURE MAP.
#   The same filter is reused everywhere (WEIGHT SHARING), so CNNs need far
#   fewer parameters than dense layers on raw pixels.
# - Early filters detect edges; deeper layers combine them into textures,
#   parts and objects.
# - Hyperparameters: kernel_size, stride (step), padding (keep the size),
#   number of output channels (filters).
#   Output size = (input + 2*padding - kernel) / stride + 1.
# - POOLING (max/avg) downsamples feature maps.
# - Typical design: [Conv -> ReLU -> Pool] x N -> Flatten -> Linear.
# - PyTorch image tensors: (batch, channels, height, width).
# - TRANSFER LEARNING: reuse a CNN pretrained on millions of images and
#   fine-tune only the last layers on your small dataset.
#
# REAL-WORLD ANALOGY
# Scanning a page with a magnifying glass that only recognises one pattern
# (say, a vertical stroke) and marking every place you see it.
#
# SYNTAX:
#   nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
#   nn.MaxPool2d(2); nn.Flatten()
#
# SMALL WORKING EXAMPLE:
import torch
import torch.nn.functional as F
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from torch import nn

torch.manual_seed(0)
image = torch.zeros(1, 1, 6, 6)
image[..., :, 3:] = 1.0
vertical_edge = torch.tensor([[[[-1.0, 0.0, 1.0]] * 3]])
print("edge detector response:\n", F.conv2d(image, vertical_edge)[0, 0])
X, y = load_digits(return_X_y=True)
X = torch.tensor(X / 16.0, dtype=torch.float32).reshape(-1, 1, 8, 8)
y = torch.tensor(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
cnn = nn.Sequential(
    nn.Conv2d(1, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
    nn.Flatten(), nn.Linear(32 * 2 * 2, 10),
)
print("shape after conv blocks:", cnn[:6](X_train[:1]).shape)
print("parameters:", sum(p.numel() for p in cnn.parameters()))
optimizer = torch.optim.Adam(cnn.parameters(), lr=3e-3)
for epoch in range(15):
    cnn.train()
    for i in range(0, len(X_train), 64):
        optimizer.zero_grad()
        loss = F.cross_entropy(cnn(X_train[i:i + 64]), y_train[i:i + 64])
        loss.backward()
        optimizer.step()
cnn.eval()
with torch.no_grad():
    print("test accuracy:", (cnn(X_test).argmax(1) == y_test).float().mean().item())

# EXPLANATION (LINE BY LINE):
# image: left half 0, right half 1 -> one vertical edge.
# vertical_edge kernel [-1, 0, 1]  -> responds where brightness increases to the right.
# F.conv2d output                  -> large values only at the edge columns.
# digits reshaped to (N, 1, 8, 8)  -> batch, channel, height, width.
# Conv(1->16) ReLU Pool -> 4x4; Conv(16->32) ReLU Pool -> 2x2; Flatten -> 128 values.
# cnn[:6](...)                     -> run only the first 6 layers to inspect the shape.
# Training loop with manual slicing for batches; F.cross_entropy on logits.
# Test accuracy ~0.97+ with only a few thousand parameters.
#
# COMMON MISTAKES:
# 1. Channels-last images (H, W, C) fed to PyTorch (expects C, H, W).
# 2. Miscomputing the flattened size (print shapes!).
# 3. Training big CNNs from scratch on tiny datasets (use transfer learning).
# 4. Forgetting to normalise pixel values.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Using the output-size formula, compute by hand the output shape of a 28x28
# image after Conv2d(k=5, padding=0), MaxPool2d(2), Conv2d(k=3, padding=1).
# Verify with PyTorch using a random tensor.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Visualise the 16 learned filters of the first conv layer (3x3 each) and the
# 16 feature maps for one digit using matplotlib subplots. Comment on what
# patterns some filters respond to.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Compare a dense network and the CNN on the digits data when test images are
# shifted by 1 pixel (torch.roll). Measure the accuracy drop for each and
# explain the result. Bonus: add random-shift augmentation during training.

# YOUR CODE:

