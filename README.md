```markdown
# AI Text Analyzer API

A production-style AI backend service that demonstrates how modern AI systems are designed, operated, and deployed.

The service exposes a secure, versioned API for hybrid text analysis, combining deterministic classical NLP with optional LLM-based analysis, with an emphasis on reliability, cost control, and backend best practices.

---

## Overview

* Classical NLP analysis runs on every request (fast, deterministic, zero cost)
* LLM analysis is optional and quota-controlled per API key
* All analysis results are persisted and can be queried via the API
* The system is fully containerized and deployment-ready

---

## Architecture

* Client sends requests to a FastAPI service running in Docker
* Requests are authenticated using HMAC-hashed API keys
* Classical NLP analysis runs on every request
* Optional LLM analysis is performed with quota enforcement
* Results and metadata are persisted in PostgreSQL (Dockerized via docker-compose)

---

## Key Features

* Versioned REST API (`/api/v1`)
* Secure API key generation and authentication
* Hybrid NLP pipeline (classical + optional LLM)
* Per–API-key daily LLM quotas
* Request tracing via unique request IDs
* LLM latency tracking
* Fault-tolerant LLM integration with graceful degradation
* Persistent storage of all analyses
* Fully Dockerized local and production setup

---

## API Endpoints

### Generate API Key
Create a new API key (returned once).

```http
POST /api/v1/keys

```

---

### Analyze Text

Perform classical NLP analysis with optional LLM-based enrichment.

```http
POST /api/v1/analyze
x-api-key: <your-api-key>

```

**Request body:**

```json
{
  "text": "This system works reliably and efficiently.",
  "use_llm": true
}

```

---

### Retrieve Analysis History

Fetch previously processed analyses with pagination.

```http
GET /api/v1/history?limit=10&offset=0
x-api-key: <your-api-key>

```

---


## Example Response

```json
{
  "request_id": "9c8e2b6f-1d7a-4b5a-9a9c-8d1f3c2e4a12",
  "word_count": 6,
  "char_count": 42,
  "sentiment": {
    "label": "positive",
    "score": 0.64
  },
  "llm": {
    "sentiment": "positive",
    "tone": "confident",
    "explanation": "The language expresses clear satisfaction and reliability.",
    "latency_ms": 387
  },
  "model": {
    "type": "openai",
    "name": "gpt-4o-mini",
    "version": "1.0"
  }
}

```

---

## Tech Stack

* **Backend:** FastAPI, SQLAlchemy
* **Database:** PostgreSQL (Dockerized via docker-compose)
* **AI:** NLTK (VADER), OpenAI API
* **Infrastructure:** Docker, Docker Compose
* **Observability:** Structured logging, request IDs, latency metrics
* **Security:** HMAC-hashed API keys

---

## Local Development

### Prerequisites

* Docker
* Docker Compose

### Run locally

```bash
docker-compose up --build

```

The API will be available at:

```
http://localhost:8000

```

Interactive API documentation:

```
http://localhost:8000/docs

```

PostgreSQL runs as a container defined in `docker-compose.yml`; no local database installation is required.

---

## Project Intent

This project was built to demonstrate AI engineering in a production context, with emphasis on system design, API contracts, operational constraints around LLMs, observability, and deployment realism.

It is intentionally not a notebook-based or UI-driven demo.

---

## Status

Core functionality is complete and production-ready.
Future work focuses on retrieval systems, async processing, and evaluation pipelines.

```

```