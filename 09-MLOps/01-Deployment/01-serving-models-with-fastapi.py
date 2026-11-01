# ======================================
# TOPIC: SERVING MODELS WITH FASTAPI
# LEVEL: INTERMEDIATE
# ID: mlops.deployment.fastapi-serving
# ======================================

# INTRODUCTION
# A model in a notebook helps nobody. Serving it behind an HTTP API lets web
# apps, mobile apps and other services use it. FastAPI is the standard Python
# framework for ML and LLM APIs.
#
# THEORY
# - FastAPI builds APIs from Python functions with type hints; Pydantic models
#   validate request and response bodies automatically and generate OpenAPI
#   docs (/docs).
# - Load the model ONCE at startup (lifespan), not per request.
# - Endpoints: POST /predict (inputs -> prediction), GET /health (for load
#   balancers), optionally GET /version (model + code version).
# - Validate inputs strictly (ranges, lengths); return clear 4xx errors.
# - async endpoints for I/O-bound work (LLM API calls); CPU-heavy inference
#   should run in a thread pool or a separate worker/service.
# - Run with an ASGI server: uvicorn app:app --host 0.0.0.0 --port 8000.
# - Test with TestClient (no real server needed).
#
# REAL-WORLD ANALOGY
# A restaurant kitchen with a service window: the chef (model) stays in the
# kitchen; waiters (API) take well-formed orders, reject impossible ones, and
# deliver dishes in a standard format.
#
# SYNTAX:
#   @app.post("/predict", response_model=Prediction)
#   def predict(request: PredictRequest) -> Prediction: ...
#
# SMALL WORKING EXAMPLE:
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

MODEL_VERSION = "iris-logreg-1.0.0"
state = {}

@asynccontextmanager
async def lifespan(app):
    data = load_iris()
    state["model"] = LogisticRegression(max_iter=1000).fit(data.data, data.target)
    state["classes"] = list(data.target_names)
    yield
    state.clear()

app = FastAPI(title="Iris classifier", lifespan=lifespan)

class PredictRequest(BaseModel):
    sepal_length: float = Field(gt=0, lt=20)
    sepal_width: float = Field(gt=0, lt=20)
    petal_length: float = Field(gt=0, lt=20)
    petal_width: float = Field(gt=0, lt=20)

class Prediction(BaseModel):
    label: str
    probability: float
    model_version: str

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": "model" in state}

@app.post("/predict", response_model=Prediction)
def predict(request: PredictRequest):
    features = [[request.sepal_length, request.sepal_width, request.petal_length, request.petal_width]]
    probabilities = state["model"].predict_proba(features)[0]
    best = int(probabilities.argmax())
    return Prediction(label=state["classes"][best], probability=round(float(probabilities[best]), 3),
                      model_version=MODEL_VERSION)

with TestClient(app) as client:
    print(client.get("/health").json())
    print(client.post("/predict", json={"sepal_length": 5.1, "sepal_width": 3.5,
                                        "petal_length": 1.4, "petal_width": 0.2}).json())
    bad = client.post("/predict", json={"sepal_length": -1, "sepal_width": 3.5, "petal_length": 1.4})
    print(bad.status_code, [e["loc"][-1] for e in bad.json()["detail"]])

# EXPLANATION (LINE BY LINE):
# lifespan                   -> runs once at startup: trains/loads the model into state.
# PredictRequest             -> request schema with range checks (Field(gt=0, lt=20)).
# Prediction                 -> response schema, including the model version.
# /health                    -> lets infrastructure check the service is ready.
# /predict                   -> validated input -> predict_proba -> structured response.
# TestClient(app)            -> exercises the API in-process (also triggers lifespan).
# Bad request                -> 422 with the exact invalid/missing fields.
# To run for real: uvicorn module:app --reload (save this code as app.py first).
#
# COMMON MISTAKES:
# 1. Loading the model inside the request handler (slow on every call).
# 2. No input validation (garbage in, confident garbage out).
# 3. Blocking CPU-heavy work inside async endpoints.
# 4. Not returning a model version (impossible to debug predictions later).

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Add a GET /version endpoint returning the model version and the list of
# classes. Test it with TestClient.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Add POST /predict/batch accepting up to 100 items, returning a list of
# predictions; reject larger batches with a 413 error. Measure the time per
# item for batch vs single requests.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Build an LLM endpoint POST /classify-ticket that calls the course LLM helper
# (offline mock by default), validates the model's JSON with Pydantic, logs
# latency and prompt version per request, and has pytest tests using
# TestClient with the LLM call mocked.

# YOUR CODE:

