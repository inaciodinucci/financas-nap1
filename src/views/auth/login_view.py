"""
Interface de Login Simples
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class LoginView(QWidget):
    login_successful = pyqtSignal(int)  # user_id
    show_register = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Finanças Pessoais")
        self.setFixedSize(500, 400)  # Tamanho mais adequado
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(25)  # Espaçamento adequado
        layout.setContentsMargins(50, 50, 50, 50)  # Margens adequadas
        
        # Título
        title = QLabel("Finanças Pessoais")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))  # Fonte adequada
        title.setStyleSheet("color: #333; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Campo email
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Arial", 12))  # Fonte adequada
        layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email")
        self.email_input.setFont(QFont("Arial", 12))  # Fonte adequada
        self.email_input.setMinimumHeight(40)  # Altura adequada
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        layout.addWidget(self.email_input)
        
        # Campo senha
        password_label = QLabel("Senha:")
        password_label.setFont(QFont("Arial", 12))  # Fonte adequada
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 12))  # Fonte adequada
        self.password_input.setMinimumHeight(40)  # Altura adequada
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        layout.addWidget(self.password_input)
        
        # Botão login
        self.login_button = QPushButton("Entrar")
        self.login_button.setFont(QFont("Arial", 14, QFont.Bold))  # Fonte adequada
        self.login_button.setMinimumHeight(45)  # Altura adequada
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        # Link para registro
        register_layout = QHBoxLayout()
        register_layout.addStretch()
        
        register_text = QLabel("Não tem conta?")
        register_text.setFont(QFont("Arial", 12))  # Fonte adequada
        register_text.setStyleSheet("color: #666;")
        register_layout.addWidget(register_text)
        
        self.register_link = QLabel("Cadastre-se")
        self.register_link.setFont(QFont("Arial", 12))  # Fonte adequada
        self.register_link.setStyleSheet("color: #007bff; text-decoration: underline; cursor: pointer; font-weight: bold;")
        self.register_link.mousePressEvent = lambda e: self.show_register.emit()
        register_layout.addWidget(self.register_link)
        
        layout.addLayout(register_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
            
        # Aqui você conectaria com o controller
        # Por enquanto, simula login bem-sucedido
        QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
        self.login_successful.emit(1)  # user_id = 1
        
    def clear_form(self):
        self.email_input.clear()
        self.password_input.clear() 