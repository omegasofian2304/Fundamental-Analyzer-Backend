from fastapi import FastAPI

app = FastAPI(title="Fundamental Analyzer API")

@app.get("/")
def root():
    return {"status": "ok"}