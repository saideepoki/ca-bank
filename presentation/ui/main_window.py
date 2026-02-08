from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QListWidget
)
from PyQt6.QtCore import Qt

from sqlalchemy.orm import Session
from sqlalchemy import select

from domain.value_objects.roles import Roles
from infrastructure.database.models import Client


class MainWindow(QMainWindow):
    def __init__(self, user, db):
        super().__init__()

        self.user = user
        self.db = db

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

        if user.role != Roles.ADMIN:
            warning = QLabel("⚠ Limited access (Staff user)")
            warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
            warning.setStyleSheet("color: red;")
            layout.addWidget(warning)

        layout.addWidget(QLabel("Clients"))

        self.client_list = QListWidget()
        self.load_clients()
        layout.addWidget(self.client_list)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def load_clients(self):
        self.client_list.clear()

        with Session(self.db.engine) as session:
            clients = session.scalars(select(Client)).all()

            for client in clients:
                self.client_list.addItem(client.name)
