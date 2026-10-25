from fastapi import FastAPI
from app.api.routers import companies, score, price, history
from app.api.error_handlers import register_error_handlers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fundamental Analyzer API")

register_error_handlers(app)

app.include_router(companies.router)
app.include_router(score.router)
app.include_router(price.router)
app.include_router(history.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}