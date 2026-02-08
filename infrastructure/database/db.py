from sqlalchemy import create_engine, inspect, text
from pathlib import Path

from infrastructure.database.models import Base

class Database:
    """
    Responsible only for database connection.
    No models, no business logic.
    """

    def __init__(self, data_dir: Path):
        self.db_path = data_dir / "bank_recon.db"
        self.engine = create_engine(f"sqlite:///{self.db_path}")

    def initialize(self):
        """
         Create all tables if they do not exist.
        """
        Base.metadata.create_all(self.engine)

        self._run_migrations()

    def _run_migrations(self):
        inspector = inspect(self.engine)

        if "users" in inspector.get_table_names():
            columns = [col["name"] for col in inspector.get_columns("users")]

            if "password_hash" not in columns:
                with self.engine.connect() as conn:
                    conn.execute(
                        text("ALTER TABLE users ADD COLUMN password_hash TEXT")
                    )
