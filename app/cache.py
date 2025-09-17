import json
import redis.asyncio as redis
from typing import Optional, Dict, Any

from app.config import settings

redis_pool: Optional[redis.Redis] = None


async def init_redis_pool():
    """
    Initializes the Redis connection pool.
    This is called once when the FastAPI application starts.
    """
    global redis_pool
    if redis_pool is None:
        redis_pool = redis.from_url(
            settings.REDIS_URL, encoding="utf-8", decode_responses=True
        )


async def close_redis_pool():
    """
    Closes the Redis connection pool.
    This is called once when the FastAPI application shuts down.
    """
    if redis_pool:
        await redis_pool.close()


async def get_link_from_cache(short_code: str) -> Optional[Dict[str, Any]]:
    cached_data = await redis_pool.get(short_code)
    if cached_data:
        return json.loads(cached_data)
    return None


async def set_link_in_cache(short_code: str, link_id: int, original_url: str):
    cache_data = {"link_id": link_id, "original_url": original_url}
    await redis_pool.set(short_code, json.dumps(cache_data), ex=3600)
