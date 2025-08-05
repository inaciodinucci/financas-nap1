"""
Dashboard Simples
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class DashboardView(QMainWindow):
    """Dashboard principal do sistema"""
    
    # Sinais para comunicação com o controlador
    logout_requested = pyqtSignal()
    add_transaction_requested = pyqtSignal()
    view_transactions_requested = pyqtSignal()
    view_reports_requested = pyqtSignal()
    view_settings_requested = pyqtSignal()
    
    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.setup_ui()
        
    def setup_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("Dashboard - Finanças Pessoais")
        self.setFixedSize(800, 600)  # Tamanho adequado
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)  # Margens adequadas
        main_layout.setSpacing(30)  # Espaçamento adequado
        
        # Header
        self.create_header(main_layout)
        
        # Cards de resumo
        self.create_summary_cards(main_layout)
        
        # Botões de ação
        self.create_action_buttons(main_layout)
        
        # Status
        status_label = QLabel("Sistema funcionando normalmente")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFont(QFont("Arial", 12))
        status_label.setStyleSheet("color: #666; font-size: 12px; padding: 10px;")
        main_layout.addWidget(status_label)
        
        main_layout.addStretch()
        
    def create_header(self, parent_layout):
        """Cria o cabeçalho"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 20, 30, 20)
        header_layout.setSpacing(10)
        
        # Título
        title_label = QLabel("Finanças Pessoais")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))  # Fonte adequada
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        
        # Mensagem de boas-vindas
        welcome_label = QLabel(f"Bem-vindo(a), {self.user_data.get('name', 'Usuário')}!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 14))  # Fonte adequada
        welcome_label.setStyleSheet("color: #666;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(welcome_label)
        
        parent_layout.addWidget(header_frame)
        
    def create_summary_cards(self, parent_layout):
        """Cria os cards de resumo"""
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)  # Espaçamento adequado
        
        # Card de Saldo
        balance_card = self.create_card("Saldo Atual", "R$ 0,00", "#28a745")
        
        # Card de Receitas
        income_card = self.create_card("Receitas", "R$ 0,00", "#17a2b8")
        
        # Card de Despesas
        expense_card = self.create_card("Despesas", "R$ 0,00", "#dc3545")
        
        cards_layout.addWidget(balance_card)
        cards_layout.addWidget(income_card)
        cards_layout.addWidget(expense_card)
        
        parent_layout.addLayout(cards_layout)
        
    def create_card(self, title: str, value: str, color: str) -> QFrame:
        """Cria um card de resumo"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border: 2px solid #ddd;
                padding: 20px;
            }}
            QFrame:hover {{
                border-color: {color};
            }}
        """)
        card.setMinimumHeight(120)  # Altura adequada
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Título
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))  # Fonte adequada
        title_label.setStyleSheet(f"color: {color};")
        
        # Valor
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(QFont("Arial", 18, QFont.Bold))  # Fonte adequada
        value_label.setStyleSheet("color: #333;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        return card
        
    def create_action_buttons(self, parent_layout):
        """Cria os botões de ação"""
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(15)  # Espaçamento adequado
        
        # Título
        actions_title = QLabel("Ações Disponíveis")
        actions_title.setAlignment(Qt.AlignCenter)
        actions_title.setFont(QFont("Arial", 16, QFont.Bold))  # Fonte adequada
        actions_title.setStyleSheet("color: #333; margin-bottom: 10px;")
        buttons_layout.addWidget(actions_title)
        
        # Botões
        self.add_transaction_btn = self.create_button("Nova Transação", "#28a745")
        self.add_transaction_btn.clicked.connect(self.add_transaction_requested.emit)
        
        self.transactions_btn = self.create_button("Ver Transações", "#17a2b8")
        self.transactions_btn.clicked.connect(self.view_transactions_requested.emit)
        
        self.reports_btn = self.create_button("Relatórios", "#6f42c1")
        self.reports_btn.clicked.connect(self.view_reports_requested.emit)
        
        self.settings_btn = self.create_button("Configurações", "#fd7e14")
        self.settings_btn.clicked.connect(self.view_settings_requested.emit)
        
        self.logout_btn = self.create_button("Sair", "#dc3545")
        self.logout_btn.clicked.connect(self.logout_requested.emit)
        
        buttons_layout.addWidget(self.add_transaction_btn)
        buttons_layout.addWidget(self.transactions_btn)
        buttons_layout.addWidget(self.reports_btn)
        buttons_layout.addWidget(self.settings_btn)
        buttons_layout.addWidget(self.logout_btn)
        
        parent_layout.addLayout(buttons_layout)
        
    def create_button(self, text: str, color: str) -> QPushButton:
        """Cria um botão de ação"""
        button = QPushButton(text)
        button.setFont(QFont("Arial", 12, QFont.Bold))  # Fonte adequada
        button.setMinimumHeight(50)  # Altura adequada
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
            QPushButton:pressed {{
                background-color: {color}aa;
            }}
        """)
        return button 