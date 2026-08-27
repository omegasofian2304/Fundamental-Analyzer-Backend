import os
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
CACHE_TTL_HOURS = int(os.getenv("CACHE_TTL_HOURS", 24))