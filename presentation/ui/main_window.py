from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CA Bank Reconciliation")
        self.resize(900, 600)

        label = QLabel("Application shell loaded")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)
