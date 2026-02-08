import sys
from PyQt6.QtWidgets import QApplication
import structlog

from config.settings import Settings
from infrastructure.logging.logger import configure_logging
from infrastructure.database.db import Database
from presentation.ui.main_window import MainWindow


def main():
    Settings.initialize()

    configure_logging(Settings.LOG_DIR)
    log = structlog.get_logger()
    log.info("Application starting")

    db = Database(Settings.DATA_DIR)
    db.initialize()
    log.info("Database initialized", path=str(db.db_path))

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
