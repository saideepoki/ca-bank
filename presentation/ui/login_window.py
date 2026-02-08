from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

class LoginWindow(QWidget):
    def __init__(self, auth_service, on_login_success):
        super().__init__()

        self.auth_service = auth_service
        self.on_login_success = on_login_success

        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username"))
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("Password"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        user = self.auth_service.authenticate(username, password)

        if user is None:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
            return

        self.on_login_success(user)
        self.close()
