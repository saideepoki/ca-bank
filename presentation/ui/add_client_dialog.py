from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from infrastructure.database.models import Client
from sqlalchemy.orm import Session


class AddClientDialog(QDialog):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.setWindowTitle("Add Client")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Client Name"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("GST Number (optional)"))
        self.gst_input = QLineEdit()
        layout.addWidget(self.gst_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_client)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_client(self):
        name = self.name_input.text().strip()
        gst = self.gst_input.text().strip() or None

        if not name:
            QMessageBox.warning(self, "Error", "Client name is required")
            return

        client = Client(
            name=name,
            gst_number=gst
        )

        with Session(self.db.engine) as session:
            session.add(client)
            session.commit()

        self.accept()
