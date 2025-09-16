from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas, auth
from app.database import SessionLocal

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("", response_model=schemas.Link, status_code=status.HTTP_201_CREATED)
async def create_short_link(
    link: schemas.LinkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    return await crud.create_short_link(db=db, link=link, user_id=current_user.id)


@router.get("/{short_code}/analytics", response_model=schemas.LinkWithAnalytics)
async def get_link_analytics_endpoint(
    short_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    db_link = await crud.get_link_by_short_code(db, short_code=short_code)

    if db_link is None:
        raise HTTPException(status_code=404, detail="Link not found")

    if db_link.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view analytics for this link"
        )

    analytics_data = await crud.get_link_analytics(db, link_id=db_link.id)

    response_data = schemas.Link.from_orm(db_link).dict()
    response_data["analytics"] = analytics_data

    return response_data
