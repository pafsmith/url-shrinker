from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, ForeignKey, Text
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Link(Base):
    __tablename__ = "links"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    visit_count = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Click(Base):
    __tablename__ = "clicks"
    id = Column(BigInteger, primary_key=True, index=True)
    link_id = Column(BigInteger, ForeignKey("links.id"), nullable=False, index=True)
    clicked_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
