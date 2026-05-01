# Task 0 - Minimal MLOps Batch Job

**Author:** Jeet Bhardwaj  
**Enrollment:** 0901AD231032  

## Overview
This repository contains a deterministic, production-ready MLOps batch job. It computes a rolling mean on the closing prices of an OHLCV dataset and generates trading signals based on that mean. 

The pipeline is designed with robust error handling, specifically engineered to bypass and sanitize heavily malformed CSV inputs (e.g., invisible quotes, trailing spaces, varying delimiters) to ensure high reliability in production.

## Features
- **Data Sanitization:** Aggressive CSV parsing that strips invisible characters and standardizes headers, preventing pipeline failures from poorly formatted flat files.
- **Container Security:** The Docker container is configured to run under a non-root `appuser`, adhering to cloud security best practices.
- **Developer Experience (Makefile):** Standardized build, run, and clean commands for seamless cross-team collaboration.
- **Deterministic Output:** Fully reproducible mathematical results governed by the injected YAML config seed.

---

## Repository Structure
- `run.py`: The procedural batch job script.
- `Dockerfile`: Instructions to build the secure, zero-argument container.
- `Makefile`: Developer shortcuts for building and testing.
- `requirements.txt`: Python dependencies.
- `config.yaml`: Configuration parameters for execution.
- `data.csv`: The input dataset.
- `metrics.json`: Sample output from a successful run.
- `run.log`: Sample execution log.

---

## Local Execution

1. **Install dependencies:**
   
```bash
   pip install -r requirements.txt
```
2. **Run the pipeline**

```bash
    python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```
## Docker Execution

The container natively maps the required command-line arguments to the internally copied files, completely fulfilling the strict zero-argument Docker requirement.

### Using the included Makefile (Recommended)

**Build the image:**
```bash
make build
```

**Run the image:**
```bash
make run
```

**Clean up outputs:**
```bash
make clean
```

---

### anual Docker Commands (Evaluation standard)

**Build the image:**
```bash
docker build -t mlops-task .
```

**Run the container:**
```bash
docker run --rm mlops-task
```

---

## Example Output (`metrics.json`)

Generated upon a successful run:

```json
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4991,
    "latency_ms": 144,
    "seed": 42,
    "status": "success"
}
```
