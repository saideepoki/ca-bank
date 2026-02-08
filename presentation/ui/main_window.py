from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QListWidgetItem
)
from PyQt6.QtCore import Qt

from sqlalchemy.orm import Session
from sqlalchemy import select

from domain.value_objects.roles import Roles
from infrastructure.database.models import Client
from presentation.ui.add_client_dialog import AddClientDialog



class MainWindow(QMainWindow):
    def __init__(self, user, db):
        super().__init__()

        self.user = user
        self.db = db
        self.active_client = None

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
        
        if user.role == Roles.ADMIN:
            add_client_btn = QPushButton("Add Client")
            add_client_btn.clicked.connect(self.open_add_client)
            layout.addWidget(add_client_btn)
        
        self.active_client_label = QLabel("Active Client: None")
        self.active_client_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.active_client_label)

        layout.addWidget(QLabel("Clients"))

        self.client_list = QListWidget()
        self.client_list.itemSelectionChanged.connect(self.on_client_selected)
        self.load_clients()
        layout.addWidget(self.client_list)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def load_clients(self):
        self.client_list.clear()
        self.active_client = None
        self.active_client_label.setText("Active Client: None")

        with Session(self.db.engine) as session:
            clients = session.scalars(select(Client)).all()

            for client in clients:
                item = QListWidgetItem(client.name)
                item.setData(Qt.ItemDataRole.UserRole, client.id)
                self.client_list.addItem(item)

    
    def open_add_client(self):
        dialog = AddClientDialog(self.db)

        if dialog.exec():
            self.load_clients()
    
    def on_client_selected(self):
        items = self.client_list.selectedItems()
        if not items:
            return

        item = items[0]
        client_id = item.data(Qt.ItemDataRole.UserRole)

        with Session(self.db.engine) as session:
            client = session.get(Client, client_id)

            if client:
                self.active_client = client
                self.active_client_label.setText(
                    f"Active Client: {client.name}"
                )
