from pathlib import Path

class Settings:
    """
    Central configuration for the application.

    This class is intentionally simple for now.
    It will grow as we add database, logging, security, etc.
    """

    APP_NAME = "CA Bank Reconciliation"

    # Base directory for all app data (safe, local, user-specific)
    BASE_DIR = Path.home() / ".ca_bank_recon"

    # Sub-directories (not used yet, but created early)
    DATA_DIR = BASE_DIR / "data"
    LOG_DIR = BASE_DIR / "logs"

    @classmethod
    def initialize(cls):
        """
        Ensure required directories exist.
        Safe to call multiple times.
        """
        cls.BASE_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOG_DIR.mkdir(exist_ok=True)
