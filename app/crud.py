from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, cast, Date
from passlib.context import CryptContext
from typing import Union

from datetime import date, timedelta
from . import models, schemas, utils


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_link_by_short_code(db: AsyncSession, short_code: str):
    """Fetches a link from the database by its short code."""
    result = await db.execute(
        select(models.Link).filter(models.Link.short_code == short_code)
    )
    return result.scalar_one_or_none()


async def get_link_by_original_url(db: AsyncSession, original_url: str):
    """Checks if a URL has already been shortened."""
    result = await db.execute(
        select(models.Link).filter(models.Link.original_url == original_url)
    )
    return result.scalar_one_or_none()


async def create_short_link(
    db: AsyncSession, link: schemas.LinkCreate, user_id: Union[int, None] = None
) -> models.Link:
    """
    Creates a new short link in the database, handling collisions.
    """
    # 1. Check if the URL has already been shortened.
    existing_link = await get_link_by_original_url(db, str(link.original_url))
    if existing_link:
        return existing_link

    # 2. Generate an initial short code.
    short_code = utils.generate_short_code(str(link.original_url))

    # 3. Collision check loop.
    collision_count = 0
    while await get_link_by_short_code(db, short_code):
        collision_count += 1
        # If a collision occurs, append a salt and re-hash.
        salt = str(collision_count)
        short_code = utils.generate_short_code(str(link.original_url), salt)

    # 4. Create the new link object.
    db_link = models.Link(
        original_url=str(link.original_url), short_code=short_code, user_id=user_id
    )

    # 5. Add to session and commit to the database.
    db.add(db_link)
    await db.commit()
    await db.refresh(db_link)

    return db_link


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """Creates a new user in the database with a hashed password."""
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    """Fetches a user by their email address."""
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()


async def get_user(db: AsyncSession, user_id: int):
    """Fetches a user by their ID."""
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()


async def log_click_to_db(
    db: AsyncSession, link_id: int, ip_address: str, user_agent: str
):
    """Logs a single click event to the database."""
    db_click = models.Click(
        link_id=link_id, ip_address=ip_address, user_agent=user_agent
    )

    try:
        db.add(db_click)

        link_to_update = await db.get(models.Link, link_id)
        if link_to_update:
            link_to_update.visit_count += 1

        await db.commit()
    except Exception as e:
        await db.rollback()
        print(f"Error logging click: {e}")


async def get_link_analytics(db: AsyncSession, link_id: int):
    total_clicks_query = select(func.count(models.Click.id)).where(
        models.Click.link_id == link_id
    )
    total_clicks_result = await db.execute(total_clicks_query)
    total_clicks = total_clicks_result.scalar_one_or_none() or 0

    thirty_days_ago = date.today() - timedelta(days=30)
    clicks_by_day_query = (
        select(
            cast(models.Click.clicked_at, Date).label("date"),
            func.count(models.Click.id).label("count"),
        )
        .where(models.Click.link_id == link_id)
        .where(cast(models.Click.clicked_at, Date) >= thirty_days_ago)
        .group_by(cast(models.Click.clicked_at, Date))
        .order_by(cast(models.Click.clicked_at, Date))
    )

    clicks_by_day_result = await db.execute(clicks_by_day_query)
    clicks_by_day = clicks_by_day_result.all()

    return schemas.AnalyticsData(
        total_clicks=total_clicks,
        clicks_by_day=[
            schemas.DailyClicks(date=row.date, count=row.count) for row in clicks_by_day
        ],
    )
