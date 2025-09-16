import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import AsyncIO
from app.config import settings
from app.database import SessionLocal
from app import crud

redis_broker = RedisBroker(url=settings.REDIS_URL, middleware=[AsyncIO()])
dramatiq.set_broker(redis_broker)


@dramatiq.actor
async def log_click_task(link_id: int, ip_address: str, user_agent: str):
    print(f"Worker received job: Log click for link_id {link_id}")
    async with SessionLocal() as db:
        await crud.log_click_to_db(
            db=db, link_id=link_id, ip_address=ip_address, user_agent=user_agent
        )
    print(f"Worker finished job for link_id {link_id}")
