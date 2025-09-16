import json
import redis.asyncio as redis
from typing import Dict, Any, Optional

from app.config import settings

redis_pool = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)


async def get_link_from_cache(short_code: str) -> Optional[Dict[str, Any]]:
    cached_data = await redis_pool.get(short_code)
    if cached_data:
        return json.loads(cached_data)
    return None


async def set_link_in_cache(short_code: str, link_id: int, original_url: str):
    cache_data = {"link_id": link_id, "original_url": original_url}
    await redis_pool.set(short_code, json.dumps(cache_data), ex=3600)
