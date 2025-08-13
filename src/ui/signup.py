from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from .widgets import SimpleButton


class SignupWindow(QWidget):
    """Tela de cadastro"""

    signup_successful = pyqtSignal()
    show_login = pyqtSignal()

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(400, 550)
        self.setWindowTitle("💰 Finanças Pessoais - Cadastro")

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title_label = QLabel("💰 Finanças Pessoais")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #667eea; margin-bottom: 20px;")

        subtitle_label = QLabel("Crie sua conta")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Segoe UI", 12))
        subtitle_label.setStyleSheet("color: #666; margin-bottom: 30px;")

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome completo")
        self.nome_input.setStyleSheet(
            """
            QLineEdit { padding: 12px; border: 2px solid #e1e5e9; border-radius: 6px; font-size: 14px; background: white; }
            QLineEdit:focus { border-color: #667eea; }
            """
        )

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet(self.nome_input.styleSheet())

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.senha_input.setStyleSheet(self.nome_input.styleSheet())

        self.confirmar_senha_input = QLineEdit()
        self.confirmar_senha_input.setPlaceholderText("Confirmar senha")
        self.confirmar_senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmar_senha_input.setStyleSheet(self.nome_input.styleSheet())

        self.criar_conta_btn = SimpleButton("Criar Conta")
        self.criar_conta_btn.clicked.connect(self.criar_conta)

        self.voltar_btn = SimpleButton("Voltar ao Login")
        self.voltar_btn.setStyleSheet(
            """
            QPushButton { background-color: #6c757d; border: none; border-radius: 6px; color: white; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #5a6268; }
            """
        )
        self.voltar_btn.clicked.connect(self.voltar_login)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(self.nome_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.senha_input)
        layout.addWidget(self.confirmar_senha_input)
        layout.addWidget(self.criar_conta_btn)
        layout.addWidget(self.voltar_btn)
        layout.addStretch()

        self.setLayout(layout)

    def criar_conta(self):
        nome = self.nome_input.text().strip()
        email = self.email_input.text().strip()
        senha = self.senha_input.text().strip()
        confirmar_senha = self.confirmar_senha_input.text().strip()

        if not all([nome, email, senha, confirmar_senha]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
        if senha != confirmar_senha:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return
        if len(senha) < 6:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 6 caracteres!")
            return

        if self.db_manager.inserir_usuario(nome, email, senha):
            QMessageBox.information(self, "Sucesso", "Conta criada com sucesso! Faça login.")
            self.signup_successful.emit()
        else:
            QMessageBox.critical(self, "Erro", "Email já cadastrado ou erro ao criar conta!")

    def voltar_login(self):
        self.show_login.emit()


