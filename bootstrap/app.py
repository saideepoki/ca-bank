import sys
from PyQt6.QtWidgets import QApplication
import structlog

from config.settings import Settings
from infrastructure.logging.logger import configure_logging
from infrastructure.database.db import Database
from presentation.ui.main_window import MainWindow
from application.services.user_service import UserService
from application.services.auth_service import AuthService
from presentation.ui.login_window import LoginWindow



def main():
    Settings.initialize()

    configure_logging(Settings.LOG_DIR)
    log = structlog.get_logger()
    log.info("Application starting")

    db = Database(Settings.DATA_DIR)
    db.initialize()
    log.info("Database initialized", path=str(db.db_path))

    user_service = UserService(db)
    user_service.ensure_admin_exists()
    log.info("Admin user ensured")

    auth_service = AuthService(db)

    app = QApplication(sys.argv)

    def on_login_success(user):
      log.info("User logged in", username=user.username, role=user.role)
      app.main_window = MainWindow(user, db)
      app.main_window.show()

    login_window = LoginWindow(auth_service, on_login_success)
    login_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
