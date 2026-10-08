from fastapi import FastAPI
from app.api.routers import companies, score

app = FastAPI(title="Fundamental Analyzer API")

app.include_router(companies.router)
app.include_router(score.router)


@app.get("/")
def root():
    return {"status": "ok"}