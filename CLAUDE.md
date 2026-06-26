# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

Academic project for course **DD283 Big Data** at Universidad Autónoma del Perú. Implements a Big Data engineering pipeline for **Yape** (Peru's largest fintech, 15M users, 3.2M transactions/day) as a Partial Evaluation (Evaluación Parcial).

The assignment rubric is in [EVALUACION_PARCIAL_BIGDATA_v1.md](EVALUACION_PARCIAL_BIGDATA_v1.md). Evidence screenshots go in `screenshots/`.

## Running the Code

**No build step.** Each part runs independently:

| Part | How to Run |
| ------ | ----------- |
| P1 (Architecture) | Markdown document — no execution needed |
| P2 (Databricks) | Upload `P2_databricks_yape.ipynb` to [community.cloud.databricks.com](https://community.cloud.databricks.com) and run cells top-to-bottom |
| P3 (MongoDB Atlas) | `pip install pymongo dnspython` → `python P3_mongodb_atlas.py` (or run in Google Colab) |
| P4 (Docker MongoDB) | Start Docker Desktop, run the `docker run` command below, then `python P4_docker.py` |

**Docker commands for P4:**

```bash
docker pull mongo:7.0
docker run -d --name yape-mongo-local -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=yape2026 \
  mongo:7.0
```

## Architecture

The project uses a **medallion architecture** on Databricks and demonstrates four technology areas:

- **P1_arquitectura.md** — Written justification of 6-component system design (CockroachDB, Redis, MongoDB Atlas, Delta Lake/Databricks, Neo4j, Apache Superset), CAP Theorem analysis for Yape's payment core vs. transaction history, and NewSQL technical rationale.

- **P2_databricks_yape.ipynb** — PySpark pipeline: Cell 1 generates 2,000 synthetic transactions to `/FileStore/yape/bronze/`; Cell 2 filters/enriches to Silver layer; Cell 3 aggregates to Gold layer; Cell 4 produces a matplotlib dashboard saved to `/FileStore/yape/gold/dashboard_yape.png`.

- **P3_mongodb_atlas.py** — Connects to MongoDB Atlas (M0 free tier), inserts 5 heterogeneous merchant documents into `yape_db.comerciantes`, runs 3 queries using MongoDB operators, and executes an aggregation pipeline for revenue-by-merchant-type reporting.

- **P4_docker.py** — Connects Python to a local Docker MongoDB container (`localhost:27017`, credentials `admin:yape2026`), inserts test data, and documents Docker-vs-Atlas tradeoffs.

## Key Constraints

- **MongoDB credentials** (`admin:yape2026`) are intentionally hardcoded in P4 — this is a local-only development container documented in an academic assignment.
- **Databricks file paths** (`/FileStore/yape/bronze|silver|gold/`) are relative to the Databricks workspace; they do not map to the local filesystem.
- All Python dependencies are installed inline (`pip install pymongo dnspython`) — no requirements.txt exists.
