from fastapi import FastAPI

from app.api.routers import companies

app = FastAPI(title="Fundamental Analyzer API")

app.include_router(companies.router)


@app.get("/")
def root():
    return {"status": "ok"}