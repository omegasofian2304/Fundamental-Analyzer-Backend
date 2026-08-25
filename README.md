# Fundamental Analyzer - Backend

Backend service for **Fundamental Analyzer**, a school project that evaluates the fundamental health of publicly listed companies with a composite score (0–100) and compares its evolution against the real stock price over time.

## Overview

The application fetches fundamental data (P/E ratio, debt-to-equity, revenue growth, profit margin) and historical price data from external APIs, computes a weighted fundamental score, and persists the results so they can be tracked over a 5-year horizon and later visualized on the frontend (Vue.js).

**Score composition:**

| Factor        | Weight |
|---------------|--------|
| Valuation     | 30%    |
| Debt level    | 30%    |
| Growth        | 20%    |
| Margin        | 20%    |

Resulting label: **Undervalued** (>70) / **Fairly valued** (40–70) / **Overvalued** (<40)

## Tech stack

- **Language / Framework:** Python + FastAPI
- **Database:** MySQL (stores every computed score with its date and price, used for history and as a base for an optional ML extension)
- **External APIs:**
  - [Finnhub](https://finnhub.io) - fundamental data (`stock/metric`, annual history via `series.annual`)
  - [Twelve Data](https://twelvedata.com) - historical stock price (`time_series`)

## Architecture: layered monolith

The backend follows a **layered (monolithic) architecture** rather than microservices, since the data flow is simple and sequential and there is no need for distributed services. Each layer has a single responsibility and only talks to the layer directly below it, which keeps the codebase easy to test and to extend.

```
Request
   │
   ▼
┌─────────────┐   HTTP routing, request/response models
│   api/      │
└─────┬───────┘
      ▼
┌─────────────┐   Business logic: score calculation, orchestration
│   core/     │
└─────┬───────┘
      ▼
┌─────────────┐   External API clients & persistence (DB access)
│   data/     │
└─────────────┘
```

- **`api/`** - Presentation layer. Exposes the HTTP endpoints (FastAPI routers), validates incoming requests, and shapes the responses. It has no business logic of its own; it delegates to `core/`.
- **`core/`** - Domain / business logic layer. Contains the actual score computation (valuation, debt, growth, margin weighting) and orchestrates calls to the data layer. This is also where a future ML module would live, without needing changes to `api/` or `data/`.
- **`data/`** - Data access layer. Contains the clients that talk to external APIs (Finnhub, Twelve Data) and the database access code (MySQL). It is the only layer allowed to perform I/O with the outside world.

This separation means each layer can be modified or replaced independently, for example swapping Twelve Data for another price provider only requires changes inside `data/`.

## Project structure

```
Fundamental-Analyzer-Backend/
├── app/
│   ├── api/
│   │   ├── routers/          # FastAPI route definitions (endpoints)
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py       # Business logic: score calculation
│   ├── data/
│   │   ├── get_price_client.py  # Twelve Data client (historical prices)
│   │   └── __init__.py
│   ├── schemas/               # Pydantic models (request/response, DB schemas)
│   ├── config.py              # App configuration / settings
│   └── main.py                # FastAPI application entry point
├── .env                        # Environment variables (not committed)
├── .env.example                 # Template for required environment variables
├── .gitignore
├── README.md
└── requirements.txt
```

## Planned endpoints

| Method | Endpoint               | Description                                   |
|--------|-------------------------|------------------------------------------------|
| GET    | `/score?ticker=`        | Get the current fundamental score for a ticker |
| GET    | `/score/history?ticker=`| Get the historical scores for a ticker         |
| GET    | `/companies`            | List available companies                       |

## Setup

1. Clone the repository and create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the required API keys and database credentials.
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```