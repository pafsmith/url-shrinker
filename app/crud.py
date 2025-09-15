from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

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


async def create_short_link(db: AsyncSession, link: schemas.LinkCreate) -> models.Link:
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
    db_link = models.Link(original_url=str(link.original_url), short_code=short_code)

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
