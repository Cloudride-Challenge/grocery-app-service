# Grocery List Application - Application Service & CI/CD

This repository contains the application source code for the Grocery List Application and its fully automated **CI/CD pipeline** implemented with **GitHub Actions**.

## Application Design & Principles

The backend service is written in **Python (FastAPI)** :
- **Single Responsibility & Decoupling:** The application architecture separates the presentation layer (`main.py`) from the data access layer (`grocery_storage.py`).
- **Database Lifecycle Management:** The application automatically initializes its database schema on startup using robust, asynchronous lifespan context handlers.
- **Environment Driven:** Configuration details like database hosts, users, and passwords are dynamically parsed from environment variables, removing hardcoded secrets.

## Project Structure

- `main.py` - The main entry point, handles web routing, serving HTML forms, and API requests.
- `grocery_storage.py` - The consolidated storage component handling pool connections, schema initialization, and SQL actions (`SELECT`, `INSERT`).
- `test_main.py` - Automation test suites using `pytest` and FastAPI's `TestClient`.
- `requirements.txt` - Python runtime dependencies (`fastapi`, `uvicorn`, `psycopg2-binary`, etc.).
- `Dockerfile` - Single-stage lightweight containerization recipe optimized for rapid scaling.
- `.github/workflows/`
  - `ci.yml` - Continuous Integration logic executing on Pull Requests.
  - `cd.yml` - Continuous Deployment pipeline executing on Merges to `main`.

## Automation Pipelines (CI/CD)

### 1. Continuous Integration (CI) - `ci.yml`
- **Trigger:** Runs automatically on any **Pull Request** targeting the `main` branch.
- **Actions:** Spins up a transient virtual machine, caches and installs package dependencies, validates syntax, and triggers automatic test runners (`pytest`).
- **Branch Protection:** This pipeline is bound to GitHub's Branch Protection Rules. Merging code into `main` is completely **blocked** unless all integration checks pass with a green status.

### 2. Continuous Deployment (CD) - `cd.yml`
- **Trigger:** Runs automatically when a PR is **merged** or code is pushed directly to the `main` branch.
- **Actions:**
  1. Authenticates securely with AWS using Repository Secrets.
  2. Compiles, versions, and tags the container image with the Git Commit SHA and the `latest` tag.
  3. Pushes the Docker image into the private **AWS ECR** repository.
  4. Modifies the ECS Task Definition file dynamically with the newly minted image URL.
  5. Performs a zero-downtime **Rolling Update deployment** directly into the AWS ECS Fargate cluster.

## Local Development & Verification
To test the application locally without AWS, ensure you have a running PostgreSQL instance and execute:
```bash
export DB_HOST="localhost"
export DB_NAME="grocery_db"
export DB_USER="your_user"
export DB_PASSWORD="your_password"

pip install -r requirements.txt
uvicorn main:app --reload
```
