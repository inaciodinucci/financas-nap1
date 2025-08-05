"""
Interface de Registro Simples
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class RegisterView(QWidget):
    register_successful = pyqtSignal(int)  # user_id
    show_login = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro - Finanças Pessoais")
        self.setFixedSize(500, 500)  # Tamanho mais adequado
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Espaçamento adequado
        layout.setContentsMargins(50, 50, 50, 50)  # Margens adequadas
        
        # Título
        title = QLabel("Criar Conta")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))  # Fonte adequada
        title.setStyleSheet("color: #333; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Campo nome
        name_label = QLabel("Nome:")
        name_label.setFont(QFont("Arial", 12))  # Fonte adequada
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite seu nome completo")
        self.name_input.setFont(QFont("Arial", 12))  # Fonte adequada
        self.name_input.setMinimumHeight(40)  # Altura adequada
        self.name_input.setStyleSheet("""
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
        layout.addWidget(self.name_input)
        
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
        
        # Campo confirmar senha
        confirm_label = QLabel("Confirmar Senha:")
        confirm_label.setFont(QFont("Arial", 12))  # Fonte adequada
        layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirme sua senha")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setFont(QFont("Arial", 12))  # Fonte adequada
        self.confirm_input.setMinimumHeight(40)  # Altura adequada
        self.confirm_input.setStyleSheet("""
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
        layout.addWidget(self.confirm_input)
        
        # Botão registrar
        self.register_button = QPushButton("Criar Conta")
        self.register_button.setFont(QFont("Arial", 14, QFont.Bold))  # Fonte adequada
        self.register_button.setMinimumHeight(45)  # Altura adequada
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)
        
        # Link para login
        login_layout = QHBoxLayout()
        login_layout.addStretch()
        
        login_text = QLabel("Já tem conta?")
        login_text.setFont(QFont("Arial", 12))  # Fonte adequada
        login_text.setStyleSheet("color: #666;")
        login_layout.addWidget(login_text)
        
        self.login_link = QLabel("Faça login")
        self.login_link.setFont(QFont("Arial", 12))  # Fonte adequada
        self.login_link.setStyleSheet("color: #007bff; text-decoration: underline; cursor: pointer; font-weight: bold;")
        self.login_link.mousePressEvent = lambda e: self.show_login.emit()
        login_layout.addWidget(self.login_link)
        
        layout.addLayout(login_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def handle_register(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()
        
        if not name or not email or not password or not confirm:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
            
        if password != confirm:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return
            
        if len(password) < 6:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 6 caracteres!")
            return
            
        # Aqui você conectaria com o controller
        # Por enquanto, simula registro bem-sucedido
        QMessageBox.information(self, "Sucesso", "Conta criada com sucesso!")
        self.register_successful.emit(1)  # user_id = 1
        
    def clear_form(self):
        self.name_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_input.clear() 