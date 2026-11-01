# ======================================
# TOPIC: DOCKER, CONFIGURATION AND SECRETS
# LEVEL: INTERMEDIATE
# ID: mlops.deployment.docker-config
# ======================================

# INTRODUCTION
# "It works on my machine" isn't deployment. Containers package your code,
# Python version and dependencies into one image that runs the same everywhere;
# configuration and secrets come from the environment, not the code.
#
# THEORY
# DOCKER:
# - A Dockerfile describes an IMAGE: base image (python:3.12-slim), install
#   dependencies, copy code, set the start command. A CONTAINER is a running image.
# - Order layers for caching: copy requirements and install BEFORE copying
#   code (code changes more often).
# - Keep images small (slim base, no build tools at runtime), run as a
#   non-root user, add a .dockerignore (.venv, data, .git, secrets).
# - Model files: bake small ones into the image; download large ones at
#   startup from object storage, or mount a volume.
# - docker build -t app:1.0 . ; docker run -p 8000:8000 --env-file .env app:1.0
# CONFIGURATION (12-factor style):
# - Settings via environment variables, validated at startup (fail fast).
# - Secrets (API keys) from a secret manager or env vars; never in images,
#   code or Git. Different values per environment (dev/staging/prod).
#
# REAL-WORLD ANALOGY
# A shipping container: whatever is inside, every port and ship handles it the
# same way. The delivery address (configuration) is written on the outside,
# not built into the cargo.
#
# SYNTAX:
#   FROM python:3.12-slim / COPY requirements.txt . / RUN pip install -r requirements.txt
#   settings = Settings.from_env(os.environ)
#
# SMALL WORKING EXAMPLE:
import os
from dataclasses import dataclass

DOCKERFILE = """FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]"""

DOCKERIGNORE = ".venv\n__pycache__\n.git\n.env\ndata/\n*.ipynb\n"

@dataclass(frozen=True)
class Settings:
    environment: str
    model_name: str
    max_tokens: int
    anthropic_api_key: str

    @classmethod
    def from_env(cls, env):
        missing = [k for k in ("APP_ENV", "ANTHROPIC_API_KEY") if not env.get(k)]
        if missing:
            raise RuntimeError(f"missing required environment variables: {missing}")
        settings = cls(environment=env["APP_ENV"], model_name=env.get("MODEL_NAME", "claude-opus-5-5"),
                       max_tokens=int(env.get("MAX_TOKENS", "2048")), anthropic_api_key=env["ANTHROPIC_API_KEY"])
        if settings.environment not in {"dev", "staging", "prod"}:
            raise RuntimeError(f"invalid APP_ENV {settings.environment!r}")
        return settings

    def __repr__(self):
        return (f"Settings(environment={self.environment!r}, model_name={self.model_name!r}, "
                f"max_tokens={self.max_tokens}, anthropic_api_key='***{self.anthropic_api_key[-4:]}')")

print(DOCKERFILE.splitlines()[0], "...", f"({len(DOCKERFILE.splitlines())} lines)")
print(Settings.from_env({"APP_ENV": "staging", "ANTHROPIC_API_KEY": "sk-test-1234abcd"}))
try:
    Settings.from_env({"APP_ENV": "prod"})
except RuntimeError as error:
    print("startup refused:", error)
print("running in a container?", os.path.exists("/.dockerenv"))

# EXPLANATION (LINE BY LINE):
# DOCKERFILE                 -> slim base; dependencies installed before code is copied
#                               (layer caching); non-root user; health check; start command.
# DOCKERIGNORE               -> keeps the venv, secrets and data out of the image.
# Settings.from_env          -> reads configuration from the environment, validates it,
#                               and refuses to start when something required is missing.
# __repr__                   -> masks the API key so logs never print the secret.
# /.dockerenv                -> a simple way to detect running inside Docker.
#
# COMMON MISTAKES:
# 1. COPY . . before installing requirements (every code change reinstalls everything).
# 2. Baking .env files or keys into images.
# 3. Huge images with build tools, datasets and notebooks inside.
# 4. Reading config lazily so errors only appear on the first request.

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Write the Dockerfile and .dockerignore for the FastAPI iris service from the
# previous topic into a folder (pathlib) and list the commands to build and run it.

# YOUR CODE:


# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# If Docker is installed, build and run the iris service container, call
# /health and /predict with curl or urllib, and record image size and start-up
# time. Then shrink the image (multi-stage build) and compare.

# YOUR CODE:


# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Write a docker-compose.yml (as a string written to disk) with the API
# service and a Postgres + pgvector database for RAG, environment-specific
# .env files, a volume for the database, and a health-check dependency. Explain
# how secrets would be provided in production.

# YOUR CODE:

