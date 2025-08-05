from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QPushButton, QComboBox, QDateEdit, QCalendarWidget,
                             QFrame, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtGui import QFont
from datetime import datetime, date, timedelta

class DateFilterWidget(QWidget):
    """Widget customizado para filtro de datas"""
    
    # Sinais
    period_changed = pyqtSignal(str, date, date)  # period_type, start_date, end_date
    
    def __init__(self):
        super().__init__()
        self.current_period = "month"
        self.current_start_date = date.today()
        self.current_end_date = date.today()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Label
        label = QLabel("Período:")
        label.setFont(QFont("Arial", 10, QFont.Bold))
        label.setStyleSheet("color: #2c3e50;")
        
        # Combo de período
        self.period_combo = QComboBox()
        self.period_combo.addItems([
            "Hoje",
            "Esta semana", 
            "Este mês",
            "Mês anterior",
            "Este ano",
            "Personalizado"
        ])
        self.period_combo.setFont(QFont("Arial", 10))
        self.period_combo.setStyleSheet(self.get_combo_stylesheet())
        self.period_combo.currentTextChanged.connect(self.on_period_changed)
        
        # Botão de calendário personalizado
        self.custom_date_btn = QPushButton("📅")
        self.custom_date_btn.setFont(QFont("Arial", 12))
        self.custom_date_btn.setStyleSheet(self.get_button_stylesheet())
        self.custom_date_btn.clicked.connect(self.show_custom_date_dialog)
        self.custom_date_btn.setVisible(False)
        
        # Label do período atual
        self.period_label = QLabel("")
        self.period_label.setFont(QFont("Arial", 10))
        self.period_label.setStyleSheet("color: #7f8c8d;")
        self.period_label.setMinimumWidth(200)
        
        layout.addWidget(label)
        layout.addWidget(self.period_combo)
        layout.addWidget(self.custom_date_btn)
        layout.addWidget(self.period_label)
        layout.addStretch()
        
        # Configurar período inicial
        self.set_period("Este mês")
    
    def on_period_changed(self, period_text: str):
        """Chamado quando o período é alterado"""
        if period_text == "Personalizado":
            self.custom_date_btn.setVisible(True)
            self.show_custom_date_dialog()
        else:
            self.custom_date_btn.setVisible(False)
            self.set_period(period_text)
    
    def set_period(self, period_text: str):
        """Define o período baseado no texto"""
        today = date.today()
        
        if period_text == "Hoje":
            start_date = today
            end_date = today
            period_type = "today"
        elif period_text == "Esta semana":
            # Encontrar início da semana (domingo)
            days_since_sunday = today.weekday() + 1
            start_date = today - timedelta(days=days_since_sunday)
            end_date = start_date + timedelta(days=6)
            period_type = "week"
        elif period_text == "Este mês":
            start_date = date(today.year, today.month, 1)
            if today.month == 12:
                end_date = date(today.year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(today.year, today.month + 1, 1) - timedelta(days=1)
            period_type = "month"
        elif period_text == "Mês anterior":
            if today.month == 1:
                start_date = date(today.year - 1, 12, 1)
                end_date = date(today.year, 1, 1) - timedelta(days=1)
            else:
                start_date = date(today.year, today.month - 1, 1)
                end_date = date(today.year, today.month, 1) - timedelta(days=1)
            period_type = "previous_month"
        elif period_text == "Este ano":
            start_date = date(today.year, 1, 1)
            end_date = date(today.year, 12, 31)
            period_type = "year"
        else:
            return
        
        self.current_period = period_type
        self.current_start_date = start_date
        self.current_end_date = end_date
        
        self.update_period_label()
        self.period_changed.emit(period_type, start_date, end_date)
    
    def update_period_label(self):
        """Atualiza o label do período"""
        if self.current_start_date == self.current_end_date:
            period_text = self.current_start_date.strftime("%d/%m/%Y")
        else:
            period_text = f"{self.current_start_date.strftime('%d/%m/%Y')} - {self.current_end_date.strftime('%d/%m/%Y')}"
        
        self.period_label.setText(period_text)
    
    def show_custom_date_dialog(self):
        """Mostra o diálogo para seleção de datas personalizadas"""
        dialog = CustomDateDialog(self.current_start_date, self.current_end_date, self)
        if dialog.exec_() == QDialog.Accepted:
            start_date, end_date = dialog.get_selected_dates()
            self.current_start_date = start_date
            self.current_end_date = end_date
            self.current_period = "custom"
            self.update_period_label()
            self.period_changed.emit("custom", start_date, end_date)
    
    def get_current_period(self) -> tuple:
        """Retorna o período atual"""
        return self.current_period, self.current_start_date, self.current_end_date
    
    def get_combo_stylesheet(self) -> str:
        """Retorna o stylesheet para combobox"""
        return """
            QComboBox {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: white;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
            }
        """
    
    def get_button_stylesheet(self) -> str:
        """Retorna o stylesheet para botões"""
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """


class CustomDateDialog(QDialog):
    """Diálogo para seleção de datas personalizadas"""
    
    def __init__(self, start_date: date, end_date: date, parent=None):
        super().__init__(parent)
        self.start_date = start_date
        self.end_date = end_date
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface do diálogo"""
        self.setWindowTitle("Selecionar Período")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Selecione o período desejado")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        
        # Calendário
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: 1px solid #ecf0f1;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #2980b9;
            }
            QCalendarWidget QMenu {
                background-color: white;
                border: 1px solid #ecf0f1;
            }
        """)
        
        # Configurar datas iniciais
        self.calendar.setSelectedDate(QDate(self.start_date.year, self.start_date.month, self.start_date.day))
        
        # Botões
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton[text="OK"] {
                background-color: #27ae60;
                color: white;
                border: none;
            }
            QPushButton[text="OK"]:hover {
                background-color: #229954;
            }
            QPushButton[text="Cancel"] {
                background-color: #e74c3c;
                color: white;
                border: none;
            }
            QPushButton[text="Cancel"]:hover {
                background-color: #c0392b;
            }
        """)
        
        layout.addWidget(title)
        layout.addWidget(self.calendar)
        layout.addWidget(button_box)
    
    def get_selected_dates(self) -> tuple:
        """Retorna as datas selecionadas"""
        selected_date = self.calendar.selectedDate()
        selected_python_date = date(selected_date.year(), selected_date.month(), selected_date.day())
        
        # Para simplificar, vamos usar a mesma data para início e fim
        # Em uma implementação mais completa, você poderia ter dois calendários
        return selected_python_date, selected_python_date 