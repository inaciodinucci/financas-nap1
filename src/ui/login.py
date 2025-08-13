from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from .widgets import SimpleButton


class LoginWindow(QWidget):
    """Tela de login"""

    login_successful = pyqtSignal(int, str)
    show_signup = pyqtSignal()

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(400, 500)
        self.setWindowTitle("💰 Finanças Pessoais - Login")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title_label = QLabel("💰 Finanças Pessoais")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #667eea; margin-bottom: 20px;")

        subtitle_label = QLabel("Faça login para continuar")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Segoe UI", 12))
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 30px;")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet(
            """
            QLineEdit { padding: 12px; border: 2px solid #e1e5e9; border-radius: 6px; font-size: 14px; background: white; }
            QLineEdit:focus { border-color: #667eea; }
            """
        )

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.senha_input.setStyleSheet(self.email_input.styleSheet())

        self.login_btn = SimpleButton("Entrar")
        self.login_btn.clicked.connect(self.fazer_login)

        self.registro_btn = SimpleButton("Criar Conta")
        self.registro_btn.setStyleSheet(
            """
            QPushButton { background-color: #28a745; border: none; border-radius: 6px; color: white; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #218838; }
            """
        )
        self.registro_btn.clicked.connect(self.mostrar_signup)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.senha_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.registro_btn)
        layout.addStretch()

        self.setLayout(layout)

    def fazer_login(self):
        """Processa o login"""
        email = self.email_input.text().strip()
        senha = self.senha_input.text().strip()
        if not email or not senha:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
        resultado = self.db_manager.verificar_login(email, senha)
        if resultado:
            user_id, nome = resultado
            self.login_successful.emit(user_id, nome)
        else:
            QMessageBox.critical(self, "Erro", "Email ou senha incorretos!")

    def mostrar_signup(self):
        self.show_signup.emit()


