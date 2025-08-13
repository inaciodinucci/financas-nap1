from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QComboBox, QDateEdit, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

from .widgets import SimpleButton, SimpleCard


class DashboardWindow(QMainWindow):
    """Janela principal"""

    def __init__(self, user_id, nome, db_manager):
        super().__init__()
        self.user_id = user_id
        self.nome = nome
        self.db_manager = db_manager
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        self.setWindowTitle(f"💰 Finanças Pessoais - {self.nome}")
        self.setMinimumSize(1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        header = self.criar_header()
        main_layout.addWidget(header)

        from PyQt5.QtWidgets import QTabWidget
        self.tab_widget = QTabWidget()

        self.dashboard_tab = self.criar_dashboard_tab()
        self.tab_widget.addTab(self.dashboard_tab, "📊 Dashboard - Visão Geral")

        self.transacoes_tab = self.criar_transacoes_tab()
        self.tab_widget.addTab(self.transacoes_tab, "💳 Transações - Histórico Completo")

        self.nova_transacao_tab = self.criar_nova_transacao_tab()
        self.tab_widget.addTab(self.nova_transacao_tab, "➕ Nova Transação - Adicionar")

        main_layout.addWidget(self.tab_widget)

    def criar_header(self):
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)

        title_label = QLabel(f"Bem-vindo, {self.nome}! 👋")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #333;")

        logout_btn = SimpleButton("Sair")
        logout_btn.setStyleSheet(
            """
            QPushButton { background-color: #dc3545; border: none; border-radius: 6px; color: white; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #c82333; }
            """
        )
        logout_btn.clicked.connect(self.close)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(logout_btn)
        return header_widget

    def criar_dashboard_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        dashboard_title = QLabel("📊 Visão Geral das Suas Finanças")
        dashboard_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        dashboard_title.setStyleSheet("color: #333; margin-bottom: 20px; text-align: center;")
        dashboard_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(dashboard_title)

        stats_layout = QHBoxLayout()

        self.saldo_card = self.criar_stats_card("💰 Saldo Atual", "R$ 0,00", "neutral")
        self.receitas_card = self.criar_stats_card("📈 Total de Receitas", "R$ 0,00", "positive")
        self.despesas_card = self.criar_stats_card("📉 Total de Despesas", "R$ 0,00", "negative")

        stats_layout.addWidget(self.saldo_card)
        stats_layout.addWidget(self.receitas_card)
        stats_layout.addWidget(self.despesas_card)
        layout.addLayout(stats_layout)

        resumo_frame = SimpleCard()
        resumo_layout = QVBoxLayout(resumo_frame)

        resumo_title = QLabel("📋 Resumo das Suas Transações")
        resumo_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        resumo_title.setStyleSheet("color: #333; margin-bottom: 20px;")

        self.resumo_label = QLabel("Nenhuma transação encontrada")
        self.resumo_label.setStyleSheet("color: #666; font-size: 14px;")

        resumo_layout.addWidget(resumo_title)
        resumo_layout.addWidget(self.resumo_label)
        layout.addWidget(resumo_frame)
        return widget

    def criar_stats_card(self, titulo, valor, tipo):
        card = SimpleCard()
        layout = QVBoxLayout(card)
        title_label = QLabel(titulo)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 12))
        title_label.setStyleSheet("color: #666; margin-bottom: 10px;")

        value_label = QLabel(valor)
        value_label.setObjectName("value_label")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))

        if tipo == "positive":
            value_label.setStyleSheet("color: #28a745;")
        elif tipo == "negative":
            value_label.setStyleSheet("color: #dc3545;")
        else:
            value_label.setStyleSheet("color: #667eea;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return card

    def criar_transacoes_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        transacoes_title = QLabel("💳 Histórico Completo das Suas Transações")
        transacoes_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        transacoes_title.setStyleSheet("color: #333; margin-bottom: 20px; text-align: center;")
        transacoes_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(transacoes_title)

        actions_layout = QHBoxLayout()
        self.atualizar_btn = SimpleButton("🔄 Atualizar Lista")
        self.atualizar_btn.clicked.connect(self.carregar_dados)
        self.atualizar_btn.setStyleSheet(
            """
            QPushButton { background-color: #17a2b8; border: none; border-radius: 6px; color: white; padding: 8px 16px; font-weight: bold; }
            QPushButton:hover { background-color: #138496; }
            """
        )
        actions_layout.addWidget(self.atualizar_btn)
        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        self.transacoes_table = QTableWidget()
        self.transacoes_table.setColumnCount(7)
        self.transacoes_table.setHorizontalHeaderLabels([
            "Data", "Descrição", "Valor", "Tipo", "Categoria", "Editar", "Excluir"
        ])
        self.transacoes_table.setStyleSheet(
            """
            QTableWidget { background: white; border: 1px solid #e1e5e9; border-radius: 6px; gridline-color: #f0f0f0; }
            QHeaderView::section { background: #f8f9fa; padding: 8px; border: none; border-bottom: 1px solid #e1e5e9; font-weight: bold; color: #333; }
            QTableWidget::item { padding: 6px; border-bottom: 1px solid #f0f0f0; }
            """
        )
        layout.addWidget(self.transacoes_table)
        return widget

    def criar_nova_transacao_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        nova_transacao_title = QLabel("➕ Adicionar Nova Transação ao Seu Controle")
        nova_transacao_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        nova_transacao_title.setStyleSheet("color: #333; margin-bottom: 20px; text-align: center;")
        nova_transacao_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(nova_transacao_title)

        form_frame = SimpleCard()
        form_layout = QVBoxLayout(form_frame)

        form_title = QLabel("📝 Preencha os Dados da Transação")
        form_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        form_title.setStyleSheet("color: #333; margin-bottom: 20px;")
        form_layout.addWidget(form_title)

        form_layout.addWidget(QLabel("📝 Descrição da Transação:"))
        self.descricao_input = QLineEdit()
        self.descricao_input.setStyleSheet(
            """
            QLineEdit { padding: 10px; border: 2px solid #e1e5e9; border-radius: 6px; font-size: 14px; }
            QLineEdit:focus { border-color: #667eea; }
            """
        )
        form_layout.addWidget(self.descricao_input)

        form_layout.addWidget(QLabel("💰 Valor (R$):"))
        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("0.00")
        self.valor_input.setStyleSheet(self.descricao_input.styleSheet())
        form_layout.addWidget(self.valor_input)

        form_layout.addWidget(QLabel("📊 Tipo de Transação:"))
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Receita", "Despesa"])
        self.tipo_combo.setStyleSheet(
            """
            QComboBox { padding: 10px; border: 2px solid #e1e5e9; border-radius: 6px; font-size: 14px; background: white; }
            QComboBox:focus { border-color: #667eea; }
            """
        )
        form_layout.addWidget(self.tipo_combo)

        form_layout.addWidget(QLabel("🏷️ Categoria:"))
        self.categoria_input = QLineEdit()
        self.categoria_input.setStyleSheet(self.descricao_input.styleSheet())
        form_layout.addWidget(self.categoria_input)

        form_layout.addWidget(QLabel("📅 Data da Transação:"))
        self.data_input = QDateEdit()
        self.data_input.setDate(QDate.currentDate())
        self.data_input.setStyleSheet(
            """
            QDateEdit { padding: 10px; border: 2px solid #e1e5e9; border-radius: 6px; font-size: 14px; background: white; }
            QDateEdit:focus { border-color: #667eea; }
            """
        )
        form_layout.addWidget(self.data_input)

        self.salvar_btn = SimpleButton("💾 Salvar Transação")
        self.salvar_btn.clicked.connect(self.salvar_transacao)
        form_layout.addWidget(self.salvar_btn)

        layout.addWidget(form_frame)
        layout.addStretch()
        return widget

    # --- Ações ---
    def salvar_transacao(self):
        try:
            descricao = self.descricao_input.text().strip()
            valor_text = self.valor_input.text().strip()
            tipo = self.tipo_combo.currentText().lower()
            categoria = self.categoria_input.text().strip()
            data = self.data_input.date().toPyDate()
            if not all([descricao, valor_text, categoria]):
                QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
                return
            try:
                valor = float(valor_text.replace(',', '.'))
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido!")
                return
            if self.db_manager.inserir_transacao(descricao, valor, tipo, categoria, data, self.user_id):
                QMessageBox.information(self, "Sucesso", "Transação salva com sucesso!")
                self.descricao_input.clear(); self.valor_input.clear(); self.categoria_input.clear(); self.data_input.setDate(QDate.currentDate())
                self.carregar_dados()
            else:
                QMessageBox.critical(self, "Erro", "Erro ao salvar transação!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {e}")

    def carregar_dados(self):
        try:
            transacoes = self.db_manager.buscar_transacoes(self.user_id)
            receitas = sum(t[2] for t in transacoes if t[3] == 'receita')
            despesas = sum(t[2] for t in transacoes if t[3] == 'despesa')
            saldo = receitas - despesas
            saldo_label = self.saldo_card.findChild(QLabel, "value_label")
            receitas_label = self.receitas_card.findChild(QLabel, "value_label")
            despesas_label = self.despesas_card.findChild(QLabel, "value_label")
            if saldo_label: saldo_label.setText(f"R$ {saldo:.2f}")
            if receitas_label: receitas_label.setText(f"R$ {receitas:.2f}")
            if despesas_label: despesas_label.setText(f"R$ {despesas:.2f}")
            self.atualizar_tabela_transacoes(transacoes)
            self.atualizar_resumo(transacoes)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def atualizar_tabela_transacoes(self, transacoes):
        try:
            self.transacoes_table.setRowCount(len(transacoes))
            for row, t in enumerate(transacoes):
                self.transacoes_table.setItem(row, 0, QTableWidgetItem(str(t[5])))
                self.transacoes_table.setItem(row, 1, QTableWidgetItem(t[1]))
                self.transacoes_table.setItem(row, 2, QTableWidgetItem(f"R$ {t[2]:.2f}"))
                self.transacoes_table.setItem(row, 3, QTableWidgetItem(t[3].title()))
                self.transacoes_table.setItem(row, 4, QTableWidgetItem(t[4]))

                editar_btn = SimpleButton("✏️"); editar_btn.setFixedSize(60, 30)
                editar_btn.setStyleSheet("QPushButton{background-color:#ffc107;border:none;border-radius:4px;color:#333;font-weight:bold;} QPushButton:hover{background:#e0a800}")
                editar_btn.clicked.connect(lambda checked, tx=t: self.editar_transacao(tx))
                self.transacoes_table.setCellWidget(row, 5, editar_btn)

                excluir_btn = SimpleButton("🗑️"); excluir_btn.setFixedSize(60, 30)
                excluir_btn.setStyleSheet("QPushButton{background-color:#dc3545;border:none;border-radius:4px;color:white;font-weight:bold;} QPushButton:hover{background:#c82333}")
                excluir_btn.clicked.connect(lambda checked, tx=t: self.excluir_transacao(tx))
                self.transacoes_table.setCellWidget(row, 6, excluir_btn)
        except Exception as e:
            print(f"Erro ao atualizar tabela: {e}")

    def editar_transacao(self, transacao):
        try:
            from PyQt5.QtWidgets import QDialog, QFormLayout
            dialog = QDialog(self); dialog.setWindowTitle("✏️ Editar Transação"); dialog.setFixedSize(400, 300); dialog.setModal(True)
            layout = QFormLayout(dialog)
            descricao_edit = QLineEdit(transacao[1]); descricao_edit.setStyleSheet("QLineEdit{padding:8px;border:2px solid #e1e5e9;border-radius:4px;font-size:14px;} QLineEdit:focus{border-color:#667eea}")
            valor_edit = QLineEdit(str(transacao[2])); valor_edit.setStyleSheet(descricao_edit.styleSheet())
            tipo_edit = QComboBox(); tipo_edit.addItems(["Receita", "Despesa"]); tipo_edit.setCurrentText(transacao[3].title())
            tipo_edit.setStyleSheet("QComboBox{padding:8px;border:2px solid #e1e5e9;border-radius:4px;font-size:14px;}")
            categoria_edit = QLineEdit(transacao[4]); categoria_edit.setStyleSheet(descricao_edit.styleSheet())
            data_edit = QDateEdit(); data_edit.setDate(QDate.fromString(str(transacao[5]), Qt.DateFormat.ISODate)); data_edit.setStyleSheet(descricao_edit.styleSheet())
            layout.addRow("📝 Descrição:", descricao_edit)
            layout.addRow("💰 Valor:", valor_edit)
            layout.addRow("📊 Tipo:", tipo_edit)
            layout.addRow("🏷️ Categoria:", categoria_edit)
            layout.addRow("📅 Data:", data_edit)
            from PyQt5.QtWidgets import QHBoxLayout
            buttons_layout = QHBoxLayout()
            salvar_btn = SimpleButton("💾 Salvar")
            salvar_btn.clicked.connect(lambda: self.salvar_edicao_transacao(transacao[0], descricao_edit.text(), valor_edit.text(), tipo_edit.currentText().lower(), categoria_edit.text(), data_edit.date().toPyDate(), dialog))
            cancelar_btn = SimpleButton("❌ Cancelar"); cancelar_btn.setStyleSheet("QPushButton{background:#6c757d;border:none;border-radius:6px;color:white;padding:8px 16px;font-weight:bold;} QPushButton:hover{background:#5a6268}")
            cancelar_btn.clicked.connect(dialog.reject)
            buttons_layout.addWidget(salvar_btn); buttons_layout.addWidget(cancelar_btn)
            layout.addRow(buttons_layout)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao editar transação: {e}")

    def salvar_edicao_transacao(self, transacao_id, descricao, valor_text, tipo, categoria, data, dialog):
        try:
            if not all([descricao, valor_text, categoria]):
                QMessageBox.warning(self, "Erro", "Preencha todos os campos!"); return
            try:
                valor = float(valor_text.replace(',', '.'))
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido!"); return
            if self.db_manager.atualizar_transacao(transacao_id, descricao, valor, tipo, categoria, data):
                QMessageBox.information(self, "Sucesso", "Transação atualizada com sucesso!"); dialog.accept(); self.carregar_dados()
            else:
                QMessageBox.critical(self, "Erro", "Erro ao atualizar transação!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {e}")

    def excluir_transacao(self, transacao):
        try:
            from PyQt5.QtWidgets import QMessageBox
            resposta = QMessageBox.question(self, "Confirmar Exclusão", f"Tem certeza que deseja excluir a transação:\n\n📝 {transacao[1]}\n💰 R$ {transacao[2]:.2f}\n📊 {transacao[3].title()}\n🏷️ {transacao[4]}\n\nEsta ação não pode ser desfeita!", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if resposta == QMessageBox.StandardButton.Yes:
                if self.db_manager.excluir_transacao(transacao[0]):
                    QMessageBox.information(self, "Sucesso", "Transação excluída com sucesso!"); self.carregar_dados()
                else:
                    QMessageBox.critical(self, "Erro", "Erro ao excluir transação!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao excluir transação: {e}")

    def atualizar_resumo(self, transacoes):
        try:
            if not transacoes:
                self.resumo_label.setText("Nenhuma transação encontrada"); return
            receitas_count = len([t for t in transacoes if t[3] == 'receita'])
            despesas_count = len([t for t in transacoes if t[3] == 'despesa'])
            texto = f"Total de transações: {len(transacoes)}\nReceitas: {receitas_count}\nDespesas: {despesas_count}"
            self.resumo_label.setText(texto)
        except Exception as e:
            print(f"Erro ao atualizar resumo: {e}")


