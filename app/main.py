from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, models, schemas
from .database import SessionLocal, engine

# Create the FastAPI app instance
app = FastAPI(
    title="URL Shortener",
    description="A simple URL shortener API built with FastAPI.",
    version="1.0.0",
)


# This is a dependency function to get a DB session for each request.
# It ensures the session is always closed after the request is finished.
async def get_db():
    async with SessionLocal() as session:
        yield session


# --- API Endpoints ---


@app.post(
    "/api/links", response_model=schemas.Link, status_code=status.HTTP_201_CREATED
)
async def create_link(link: schemas.LinkCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new shortened link.
    """
    return await crud.create_short_link(db=db, link=link)


@app.get(
    "/{short_code}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
async def redirect_to_url(short_code: str, db: AsyncSession = Depends(get_db)):
    """
    Redirects to the original URL associated with the short code.
    """
    db_link = await crud.get_link_by_short_code(db=db, short_code=short_code)

    if db_link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short link not found."
        )

    # TODO: Asynchronously increment the visit_count here.

    return RedirectResponse(url=db_link.original_url)


@app.get("/api/links/{short_code}", response_model=schemas.Link)
async def get_link_details(short_code: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieves the details for a short link.
    """
    db_link = await crud.get_link_by_short_code(db=db, short_code=short_code)
    if db_link is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short link not found."
        )
    return db_link
