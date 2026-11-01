# ======================================
# TOPIC: FINE-TUNING AND LORA
# LEVEL: ADVANCED
# ID: generative-ai.fine-tuning.lora
# ======================================

# INTRODUCTION
# Fine-tuning adapts a pretrained model to your task by training it further
# on your examples. LoRA makes this affordable by training a tiny number of
# extra parameters instead of the whole model.
# (When to choose it: 06-Prompt-Engineering/06-Strategy.)
#
# THEORY
# - FULL fine-tuning updates all weights: expensive (memory for weights,
#   gradients and optimizer state) and produces a full model copy per task.
# - LoRA (Low-Rank Adaptation): freeze the pretrained weight W (d x k) and
#   learn a low-rank update B @ A with B (d x r), A (r x k), r small (4-64):
#   W' = W + (alpha / r) * B @ A. Only A and B are trained -> often <1% of
#   parameters. B starts at zero so training starts from the original model.
# - QLoRA: LoRA on a 4-bit quantised base model -> fits large models on one GPU.
# - Data: hundreds to thousands of high-quality input/output examples in the
#   chat format; quality beats quantity. Hold out an eval set.
# - Typical stack: Hugging Face transformers + peft + datasets (+ trl for SFT).
#   Vendor APIs offer fine-tuning for some hosted models.
# - Risks: overfitting, forgetting general abilities, maintenance when base
#   models update, and data privacy.
#
# REAL-WORLD ANALOGY
# Instead of rewriting a whole textbook (full fine-tuning), you add a slim
# booklet of corrections that is read alongside it (LoRA adapter) - cheap to
# write, easy to swap.
#
# SYNTAX:
#   layer = LoRALinear(pretrained_linear, r=4, alpha=8)
#   optimizer = AdamW([p for p in model.parameters() if p.requires_grad])
#
# SMALL WORKING EXAMPLE:
import torch
from torch import nn

torch.manual_seed(0)

class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, r=4, alpha=8):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad = False
        self.A = nn.Parameter(torch.randn(r, base.in_features) * 0.01)
        self.B = nn.Parameter(torch.zeros(base.out_features, r))
        self.scale = alpha / r

    def forward(self, x):
        return self.base(x) + (x @ self.A.T @ self.B.T) * self.scale

pretrained = nn.Sequential(nn.Linear(32, 64), nn.ReLU(), nn.Linear(64, 2))
X = torch.randn(512, 32)
y_new_task = (X[:, 0] * X[:, 1] > 0).long()
model = nn.Sequential(LoRALinear(pretrained[0]), nn.ReLU(), LoRALinear(pretrained[2]))
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"trainable {trainable} / {total} parameters ({trainable / total:.1%})")
with torch.no_grad():
    print("before training, output equals the pretrained model:", torch.allclose(model(X), pretrained(X)))
optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=1e-2)
for step in range(300):
    loss = nn.functional.cross_entropy(model(X), y_new_task)
    optimizer.zero_grad(); loss.backward(); optimizer.step()
accuracy = (model(X).argmax(1) == y_new_task).float().mean().item()
print(f"after LoRA training: loss {loss.item():.3f}, train accuracy {accuracy:.2f}")
print("base weights unchanged:", torch.equal(model[0].base.weight, pretrained[0].weight))

# EXPLANATION (LINE BY LINE):
# LoRALinear                 -> wraps a frozen Linear; adds trainable A (r x in) and
#                               B (out x r); B = 0 so the initial output is unchanged.
# forward                    -> base(x) + scaled low-rank update.
# pretrained                 -> a stand-in for a large pretrained network.
# trainable / total          -> ~22% here only because the toy layers are tiny; for a
#                               4096 x 4096 layer with r=8 it is about 0.4% (Question 1).
# allclose before training   -> confirms the adapter starts as a no-op.
# Optimizer gets only requires_grad parameters (A and B).
# base weights unchanged     -> the adapter can be removed or swapped per task.
#
# COMMON MISTAKES:
# 1. Fine-tuning to add frequently changing facts (use RAG).
# 2. Training on low-quality or inconsistent examples.
# 3. No held-out evaluation (you can't tell if it helped or overfit).
# 4. Forgetting to freeze the base model (accidental full fine-tuning).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Compute by hand the parameter count of a LoRA adapter with r=8 on a
# 4096 x 4096 weight matrix, compare with the full matrix, and verify in code.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Compare r = 1, 4, 16 on the toy task: trainable parameters, final accuracy
# on a held-out split, and training time. Add a merge() method that folds
# B @ A into the base weight for inference and verify outputs are identical.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# With Hugging Face transformers + peft (install them), apply LoRA to a small
# open model (e.g. distilbert for sentiment classification) on a public
# dataset subset. Report trainable parameters, accuracy before/after, and
# the adapter file size.

# YOUR CODE:

