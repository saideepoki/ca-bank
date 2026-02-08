from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from infrastructure.database.models import User
from infrastructure.security.password_hashing import verify_password


class AuthService:
    def __init__(self, db):
        self.db = db

    def authenticate(self, username: str, password: str) -> Optional[User]:
        with Session(self.db.engine) as session:
            user = session.scalar(
                select(User).where(User.username == username)
            )

            if user is None:
                return None

            if not user.password_hash:
                return None

            if not verify_password(user.password_hash, password):
                return None

            return user
