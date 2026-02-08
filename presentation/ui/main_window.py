from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from domain.value_objects.roles import Roles


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("CA Bank Reconciliation")
        self.resize(900, 600)

        central = QWidget()
        layout = QVBoxLayout()

        welcome = QLabel(f"Welcome, {user.username}")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        role_label = QLabel(f"Role: {user.role}")
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(welcome)
        layout.addWidget(role_label)

        # RBAC PROOF
        if user.role != Roles.ADMIN:
            warning = QLabel("⚠ Limited access (Staff user)")
            warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
            warning.setStyleSheet("color: red;")
            layout.addWidget(warning)

        central.setLayout(layout)
        self.setCentralWidget(central)
