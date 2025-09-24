from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi_limiter import FastAPILimiter
from sqlalchemy.ext.asyncio import AsyncSession

from . import cache, crud
from .database import SessionLocal
from .routers import auth as auth_router
from .routers import links as links_router
from .tasks import log_click_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application's lifespan events for startup and shutdown.
    """
    # Initialize the Redis connection pool and the rate limiter on startup
    await cache.init_redis_pool()
    await FastAPILimiter.init(cache.redis_pool)
    yield
    # Clean up the Redis connection pool on shutdown
    await cache.close_redis_pool()


# Create the FastAPI app instance
app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener API built with FastAPI.",
    version="1.0.0",
    lifespan=lifespan,
)


# This is a dependency function to get a DB session for each request.
# It ensures the session is always closed after the request is finished.
async def get_db():
    async with SessionLocal() as session:
        yield session


# --- API Endpoints ---
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(links_router.router, prefix="/api/links", tags=["Links"])


@app.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def redirect_to_url(
    short_code: str, request: Request, db: AsyncSession = Depends(get_db)
):
    """
    Redirects to the original URL associated with the short code.
    """

    link_id_to_log = None
    url_to_redirect = None

    cached_link_data = await cache.get_link_from_cache(short_code)
    if cached_link_data:
        print(f"CACHE HIT for {short_code}")
        link_id_to_log = cached_link_data.get("link_id")
        url_to_redirect = cached_link_data.get("original_url")
    else:
        print(f"CACHE MISS for {short_code}")
        db_link = await crud.get_link_by_short_code(db, short_code=short_code)
        if db_link:
            link_id_to_log = db_link.id
            url_to_redirect = db_link.original_url
            await cache.set_link_in_cache(
                short_code=db_link.short_code,
                link_id=db_link.id,
                original_url=db_link.original_url,
            )

    if not url_to_redirect or not link_id_to_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short link not found."
        )

    log_click_task.send(
        link_id_to_log,
        request.client.host,
        request.headers.get("user-agent", "Unknown"),
    )
    return RedirectResponse(url=url_to_redirect)
