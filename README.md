# Fundamental Analyzer - Backend

Backend service for **Fundamental Analyzer**, a school project that evaluates the fundamental health of publicly listed companies with a composite score (0-100) and compares its evolution against the real stock price over time.

## Overview

The application fetches fundamental data (P/E ratio, debt-to-equity, revenue growth, profit margin) and historical price data from external APIs, computes a weighted fundamental score, and persists the results so they can be tracked over a 5-year horizon and later visualized on the frontend (Vue.js).

**Score composition:**

| Factor        | Weight |
|---------------|--------|
| Valuation     | 30%    |
| Debt level    | 30%    |
| Growth        | 20%    |
| Margin        | 20%    |

Resulting label: **sous-évaluée** (>=70) / **correctement valorisée** (30-70) / **sur-évaluée** (<=30)

## Tech stack

- **Language / Framework:** Python + FastAPI
- **Database:** MySQL (stores every computed score with its date and label for historical tracking)
- **Cache:** Redis (caches S&P 500 tickers, fundamental metrics, percentile bounds and price history)
- **External APIs:**
  - [Finnhub](https://finnhub.io) - fundamental data (`stock/metric`, quarterly history via `series.quarterly`)
  - [Twelve Data](https://twelvedata.com) - historical stock price (`time_series`)

## Architecture: layered monolith

The backend follows a **layered (monolithic) architecture** rather than microservices, since the data flow is simple and sequential and there is no need for distributed services. Each layer has a single responsibility and only talks to the layer directly below it, which keeps the codebase easy to test and to extend.

```
Request
   │
   ▼
┌─────────────┐   HTTP routing, request/response models, error handling
│   api/      │
└─────┬───────┘
      ▼
┌─────────────┐   Business logic: score calculation, orchestration
│   core/     │
└─────┬───────┘
      ▼
┌─────────────┐   External API clients, cache & persistence (DB access)
│   data/     │
└─────────────┘
```

- **`api/`** - Presentation layer. Exposes the HTTP endpoints (FastAPI routers), validates incoming requests, shapes the responses, and centralizes error handling. It has no business logic of its own; it delegates to `core/`.
- **`core/`** - Domain / business logic layer. Contains the actual score computation (valuation, debt, growth, margin weighting) and orchestrates calls to the data layer. This is also where a future ML module would live, without needing changes to `api/` or `data/`.
- **`data/`** - Data access layer. Contains the clients that talk to external APIs (Finnhub, Twelve Data), the Redis cache logic, and the database access code (MySQL). It is the only layer allowed to perform I/O with the outside world.

This separation means each layer can be modified or replaced independently, for example swapping Twelve Data for another price provider only requires changes inside `data/`.

## Project structure

```
Fundamental-Analyzer-Backend/
├── app/
│   ├── api/
│   │   ├── routers/              # FastAPI route definitions (endpoints)
│   │   ├── error_handlers.py     # Centralized exception handlers
│   │   └── __init__.py
│   ├── core/
│   │   ├── score_calculator.py   # Score computation and orchestration
│   │   ├── bounds_calibration.py # Percentile bounds calculation
│   │   ├── metric_constants.py   # Metric names, weights, constants
│   │   ├── score_history.py      # Score history orchestration
│   │   ├── company.py            # Company orchestration
│   │   ├── price.py              # Price history orchestration
│   │   └── __init__.py
│   ├── data/
│   │   ├── cache/                # Redis cache logic
│   │   ├── metrics/              # Finnhub client (fundamental data)
│   │   ├── price/                # Twelve Data client (historical prices)
│   │   ├── tickers/              # S&P 500 ticker list fetcher
│   │   ├── models/               # SQLAlchemy models
│   │   ├── score_history/        # Score history DB access
│   │   ├── database.py           # SQLAlchemy engine and session
│   │   ├── fundamental_analyzer.sql  # Database schema
│   │   └── __init__.py
│   ├── schemas/                   # Pydantic models (request/response)
│   ├── scripts/
│   │   └── refresh_sp500_cache.py # CLI script to refresh S&P 500 bounds
│   ├── config.py                  # App configuration / settings
│   └── main.py                    # FastAPI application entry point
├── .env                            # Environment variables (not committed)
├── .env.example                    # Template for required environment variables
├── .gitignore
├── README.md
└── requirements.txt
```

## Endpoints

| Method | Endpoint             | Description                                      |
|--------|----------------------|--------------------------------------------------|
| GET    | `/score/{ticker}`    | Get the current fundamental score for a ticker   |
| GET    | `/history/{ticker}`  | Get the historical scores for a ticker           |
| GET    | `/price/{ticker}`    | Get the historical price data for a ticker       |
| GET    | `/companies`         | List available companies                         |

## Error handling

Errors are handled centrally via exception handlers registered on the FastAPI app:

| Exception              | HTTP code | Meaning                        |
|------------------------|-----------|--------------------------------|
| Invalid ticker format  | 400       | Ticker must be 1-5 letters     |
| MetricFetchError       | 404       | Ticker not found on Finnhub    |
| PriceHistoryError      | 404       | No price data for this ticker  |
| RedisConnectionError   | 503       | Cache (Redis) unavailable      |
| SQLAlchemyError        | 503       | Database unavailable           |
| ValueError             | 503       | Bounds not in cache            |
| Any other exception    | 500       | Internal server error          |

## Setup

1. Clone the repository and create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the required API keys and database credentials.
4. Make sure MySQL and Redis are running.
5. Run the database schema:
   ```bash
   mysql -u root -p < app/data/fundamental_analyzer.sql
   ```
6. Refresh the S&P 500 percentile bounds cache (required before first use):
   ```bash
   python -m app.scripts.refresh_sp500_cache
   ```
7. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```