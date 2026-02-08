from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    """
    pass


class User(Base):
    """
    Users of the application (admin, staff, etc.)
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=True)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
