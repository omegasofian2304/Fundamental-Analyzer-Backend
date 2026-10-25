import redis

from app.config import REDIS_URL


class RedisConnectionError(Exception):
    pass


_client = None


def get_redis():
    global _client

    if _client is None:
        _client = redis.from_url(REDIS_URL, decode_responses=True)

    return _client


def ping():
    try:
        return get_redis().ping()
    except redis.RedisError as exc:
        raise RedisConnectionError(f"Redis unreachable: {exc}")