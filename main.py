#!/usr/bin/env python3
"""
Sistema de Gestão de Finanças Pessoais
======================================

Aplicação desktop para controle financeiro pessoal desenvolvida com PyQt5 e MySQL.

Funcionalidades:
- Autenticação segura com JWT
- Dashboard com gráficos interativos
- Gestão completa de transações
- Relatórios e análises
- Interface moderna e responsiva

Autor: Sistema de Finanças Pessoais
Versão: 1.0.0
"""

import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QFont
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('financas_pessoais.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models.database import db_manager
from src.controllers.auth_controller import AuthController

class FinancasPessoaisApp:
    """Classe principal da aplicação"""
    
    def __init__(self):
        self.app = None
        self.auth_controller = None
        self.splash_screen = None
    
    def initialize_app(self):
        """Inicializa a aplicação PyQt5"""
        try:
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("Sistema de Finanças Pessoais")
            self.app.setApplicationVersion("1.0.0")
            self.app.setOrganizationName("Finanças Pessoais")
            
            # Configurar estilo global
            self.app.setStyle('Fusion')
            
            logger.info("Aplicação PyQt5 inicializada com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar aplicação PyQt5: {e}")
            return False
    
    def show_splash_screen(self):
        """Mostra a tela de splash"""
        try:
            # Criar splash screen simples
            splash_pixmap = QPixmap(400, 300)
            splash_pixmap.fill(Qt.white)
            
            self.splash_screen = QSplashScreen(splash_pixmap)
            
            # Adicionar texto ao splash
            self.splash_screen.showMessage(
                "💰 Sistema de Finanças Pessoais\n\nInicializando...",
                Qt.AlignCenter | Qt.AlignBottom,
                Qt.black
            )
            
            self.splash_screen.show()
            self.app.processEvents()
            
            logger.info("Splash screen exibida")
            
        except Exception as e:
            logger.error(f"Erro ao mostrar splash screen: {e}")
    
    def initialize_database(self):
        """Inicializa a conexão com o banco de dados"""
        try:
            self.splash_screen.showMessage(
                "💰 Sistema de Finanças Pessoais\n\nConectando ao banco de dados...",
                Qt.AlignCenter | Qt.AlignBottom,
                Qt.black
            )
            self.app.processEvents()
            
            # Tentar conectar ao banco
            if not db_manager.connect():
                raise Exception("Falha ao conectar com o banco de dados")
            
            # Criar tabelas se não existirem
            if not db_manager.create_tables():
                raise Exception("Falha ao criar tabelas do banco de dados")
            
            logger.info("Banco de dados inicializado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar banco de dados: {e}")
            self.show_database_error(str(e))
            return False
    
    def initialize_controllers(self):
        """Inicializa os controladores da aplicação"""
        try:
            self.splash_screen.showMessage(
                "💰 Sistema de Finanças Pessoais\n\nCarregando módulos...",
                Qt.AlignCenter | Qt.AlignBottom,
                Qt.black
            )
            self.app.processEvents()
            
            self.auth_controller = AuthController()
            
            logger.info("Controladores inicializados com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar controladores: {e}")
            return False
    
    def show_database_error(self, error_message: str):
        """Mostra mensagem de erro do banco de dados"""
        QMessageBox.critical(
            None,
            "Erro de Conexão",
            f"Não foi possível conectar ao banco de dados.\n\n"
            f"Erro: {error_message}\n\n"
            "Verifique:\n"
            "1. Se o MySQL está rodando\n"
            "2. Se as configurações no arquivo .env estão corretas\n"
            "3. Se o banco de dados 'personal_finance' existe\n"
            "4. Se o usuário tem permissões adequadas"
        )
    
    def show_startup_error(self, error_message: str):
        """Mostra mensagem de erro de inicialização"""
        QMessageBox.critical(
            None,
            "Erro de Inicialização",
            f"Erro ao inicializar o sistema:\n\n{error_message}"
        )
    
    def start_application(self):
        """Inicia a aplicação"""
        try:
            # Fechar splash screen
            if self.splash_screen:
                self.splash_screen.finish(None)
            
            # Mostrar tela de login
            self.auth_controller.show_login()
            
            logger.info("Aplicação iniciada com sucesso")
            
            # Executar loop principal
            return self.app.exec_()
            
        except Exception as e:
            logger.error(f"Erro ao iniciar aplicação: {e}")
            self.show_startup_error(str(e))
            return 1
    
    def run(self):
        """Executa a aplicação completa"""
        try:
            logger.info("Iniciando Sistema de Finanças Pessoais...")
            
            # 1. Inicializar aplicação PyQt5
            if not self.initialize_app():
                return 1
            
            # 2. Mostrar splash screen
            self.show_splash_screen()
            
            # 3. Carregar variáveis de ambiente
            load_dotenv()
            
            # 4. Inicializar banco de dados
            if not self.initialize_database():
                return 1
            
            # 5. Inicializar controladores
            if not self.initialize_controllers():
                return 1
            
            # 6. Iniciar aplicação
            return self.start_application()
            
        except Exception as e:
            logger.error(f"Erro fatal na aplicação: {e}")
            self.show_startup_error(str(e))
            return 1
        
        finally:
            # Cleanup
            if db_manager:
                db_manager.disconnect()
            logger.info("Aplicação finalizada")

def main():
    """Função principal"""
    app = FinancasPessoaisApp()
    return app.run()

if __name__ == "__main__":
    sys.exit(main()) 