from fastapi import FastAPI
from app.api.routers import companies, score, price

app = FastAPI(title="Fundamental Analyzer API")

app.include_router(companies.router)
app.include_router(score.router)
app.include_router(price.router)


@app.get("/")
def root():
    return {"status": "ok"}