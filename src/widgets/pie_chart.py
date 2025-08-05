from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class PieChartWidget(QWidget):
    """Widget customizado para gráfico de pizza"""
    
    def __init__(self):
        super().__init__()
        self.data = []
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface do widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título
        title = QLabel("Distribuição por Categorias")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        
        # Figura do matplotlib
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(title)
        layout.addWidget(self.canvas)
        
        # Dados iniciais vazios
        self.update_data([])
    
    def update_data(self, data: list):
        """Atualiza os dados do gráfico"""
        self.data = data
        self.draw_chart()
    
    def draw_chart(self):
        """Desenha o gráfico de pizza"""
        # Limpar figura anterior
        self.figure.clear()
        
        if not self.data:
            # Mostrar mensagem quando não há dados
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'Nenhum dado disponível', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=12, color='gray')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            # Preparar dados para o gráfico
            labels = [item['name'] for item in self.data]
            values = [item['value'] for item in self.data]
            colors = [item['color'] for item in self.data]
            
            # Criar gráfico de pizza
            ax = self.figure.add_subplot(111)
            wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors, 
                                             autopct='%1.1f%%', startangle=90)
            
            # Configurar texto
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            for text in texts:
                text.set_fontsize(10)
            
            ax.set_title('Distribuição de Despesas por Categoria', 
                        fontsize=12, fontweight='bold', pad=20)
        
        self.figure.tight_layout()
        self.canvas.draw() 