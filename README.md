# NewsLake

NewsLake is a Data Engineering project that collects news articles from multiple public APIs, normalizes the data into a unified schema, and stores it in PostgreSQL.

The pipeline is orchestrated by Apache Airflow and containerized with Docker.

## Features

* Collect news from 10+ sources
* Normalize heterogeneous API responses
* Store articles in PostgreSQL
* Scheduled ingestion with Airflow
* Adapter-based architecture for easy source extension
* Dockerized deployment

## Architecture

```text
News APIs
    ↓
Adapters
    ↓
Normalization
    ↓
PostgreSQL
    ↑
Airflow Scheduler
```

## Project Structure

```text
newslake/
├── dags/
├── src/
│   ├── adapters/
│   ├── db/
│   ├── models/
│   └── pipelines/
├── configs/
├── docker-compose.yaml
├── Dockerfile
└── requirements.txt
```

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/newslake.git
cd newslake
```

### 2. Configure Environment Variables

Create a `.env` file from `.env.example`.

```env
THENEWSAPI_KEY=
NEWSAPI_KEY=
GNEWS_API_KEY=
NEWSDATA_API_KEY=
CURRENTS_API_KEY=
FREENEWSAPI_KEY=
GUARDIAN_API_KEY=
NYT_API_KEY=
EVENT_REGISTRY_API_KEY=

DATABASE_URL=postgresql://postgres:your_password@localhost:5432/postgres
AIRFLOW_UID=50000
```

### 3. Start Airflow

```bash
docker compose up airflow-init
docker compose up -d
```

### 4. Open Airflow UI

```text
http://localhost:8080
```

Default credentials:

```text
airflow / airflow
```

Enable the `news_pipeline` DAG and trigger it manually or wait for the scheduled run.


## Adding a New Source

1. Create a new adapter in `src/adapters/`
2. Register it in `factory.py`
3. Add source configuration to `configs/api_sources.json`

No pipeline changes are required.

## License

MIT License
