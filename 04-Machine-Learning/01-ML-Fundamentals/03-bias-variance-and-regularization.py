# ======================================
# TOPIC: OVERFITTING, BIAS-VARIANCE AND REGULARIZATION
# LEVEL: INTERMEDIATE
# ID: ml.fundamentals.bias-variance
# ======================================

# INTRODUCTION
# A model can be too simple to capture the pattern (underfit) or so flexible
# it memorises noise (overfit). Managing this trade-off is the central skill
# of practical ML.
#
# THEORY
# - UNDERFITTING (high BIAS): poor on training AND validation data.
# - OVERFITTING (high VARIANCE): great on training, poor on validation.
# - Expected error = bias^2 + variance + irreducible noise.
# - Fixes for overfitting: more data, simpler model, REGULARIZATION, feature
#   selection, early stopping, ensembling/dropout (deep learning).
# - Fixes for underfitting: more features, more flexible model, less
#   regularization, train longer.
# - REGULARIZATION adds a penalty on large weights to the loss:
#   RIDGE (L2): + alpha * sum(w^2) -> shrinks weights smoothly.
#   LASSO (L1): + alpha * sum(|w|) -> pushes some weights to exactly 0.
#   Larger alpha = stronger penalty = simpler model. Scale features first.
# - LEARNING CURVES (score vs training size) and VALIDATION CURVES (score vs a
#   hyperparameter) diagnose which problem you have.
#
# REAL-WORLD ANALOGY
# A student who memorises past papers word-for-word (overfit) versus one who
# only learned the chapter titles (underfit). Regularization is the teacher
# saying "explain the idea in simple terms".
#
# SYNTAX:
#   Ridge(alpha=1.0), Lasso(alpha=0.1), PolynomialFeatures(degree=d)
#
# SMALL WORKING EXAMPLE:
import numpy as np
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

rng = np.random.default_rng(1)
x = rng.uniform(-3, 3, 60).reshape(-1, 1)
y = np.sin(x).ravel() + rng.normal(scale=0.2, size=60)
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.4, random_state=0)
for degree in [1, 4, 15]:
    model = make_pipeline(PolynomialFeatures(degree), StandardScaler(), LinearRegression())
    model.fit(x_train, y_train)
    train_mse = mean_squared_error(y_train, model.predict(x_train))
    val_mse = mean_squared_error(y_val, model.predict(x_val))
    print(f"degree {degree:>2}: train MSE {train_mse:.3f} | val MSE {val_mse:.3f}")
for name, reg in [("ridge", Ridge(alpha=1.0)), ("lasso", Lasso(alpha=0.01, max_iter=50_000))]:
    model = make_pipeline(PolynomialFeatures(15), StandardScaler(), reg).fit(x_train, y_train)
    coefs = model[-1].coef_
    print(f"degree 15 + {name}: val MSE {mean_squared_error(y_val, model.predict(x_val)):.3f}, "
          f"zero weights: {np.sum(np.isclose(coefs, 0))}/{len(coefs)}")

# EXPLANATION (LINE BY LINE):
# y = sin(x) + noise            -> a curved pattern a straight line cannot fit.
# degree 1                      -> underfits: both errors high.
# degree 4                      -> good balance: both errors low.
# degree 15                     -> overfits: tiny train error, larger val error.
# make_pipeline(PolynomialFeatures, StandardScaler, model) -> scaling before
#                                  regularization is essential.
# Ridge(alpha=1.0)              -> same degree 15, but penalised weights generalise better.
# Lasso                         -> sets many coefficients exactly to zero (feature selection).
#
# COMMON MISTAKES:
# 1. Judging complexity by training error alone.
# 2. Regularizing unscaled features (penalty affects features unequally).
# 3. Tuning alpha on the test set.
# 4. Assuming more complex models are always better.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Using the same data, loop over polynomial degrees 1..15 and print train and
# validation MSE. Which degree would you choose and why?

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Plot a validation curve for Ridge alpha (np.logspace(-4, 3, 20)) on the
# degree-15 model with sklearn.model_selection.validation_curve. Mark the
# underfitting and overfitting regions.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Estimate bias^2 and variance empirically: generate 200 different training
# sets from the same process, fit degree 1, 4 and 15 models, and at fixed test
# points compute the squared bias of the average prediction and the variance
# of predictions. Show the trade-off in a table and a plot.

# YOUR CODE:

