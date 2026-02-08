from sqlalchemy.orm import Session
from sqlalchemy import select

from infrastructure.database.models import User
from infrastructure.security.password_hashing import hash_password


class UserService:
    """
    Handles user-related application logic.
    """

    def __init__(self, db):
        self.db = db

    def ensure_admin_exists(self):
        """
        Create a default admin user if no users exist.
        """
        with Session(self.db.engine) as session:
            user_count = session.scalar(
                select(User).limit(1)
            )

            # If at least one user exists, do nothing
            if user_count is not None:
                return

            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="ADMIN"
            )

            session.add(admin)
            session.commit()
