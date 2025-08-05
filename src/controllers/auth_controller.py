from typing import Optional, Dict, Any
from ..models.user_model import UserModel
from ..views.auth.login_view import LoginView
from ..views.auth.register_view import RegisterView
from ..views.dashboard_view import DashboardView
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AuthController:
    """Controlador para autenticação e gerenciamento de usuários"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.current_user = None
        self.current_token = None
        self.login_view = None
        self.register_view = None
        self.dashboard_view = None
    
    def show_login(self):
        """Mostra a tela de login"""
        if not self.login_view:
            self.login_view = LoginView()
            self.login_view.login_successful.connect(self.handle_login_success)
            self.login_view.show_register.connect(self.show_register)
        
        self.login_view.show()
        self.login_view.raise_()
        self.login_view.activateWindow()
    
    def show_register(self):
        """Mostra a tela de registro"""
        if not self.register_view:
            self.register_view = RegisterView()
            self.register_view.register_successful.connect(self.handle_register_success)
            self.register_view.show_login.connect(self.show_login)
        
        # Esconder login se estiver visível
        if self.login_view and self.login_view.isVisible():
            self.login_view.hide()
        
        self.register_view.show()
        self.register_view.raise_()
        self.register_view.activateWindow()
    
    def handle_login_success(self, user_id: int):
        """Processa login bem-sucedido"""
        try:
            # Buscar dados do usuário
            user = self.user_model.get_user_by_id(user_id)
            if not user:
                # Se não encontrar no banco, criar usuário simulado
                user = {
                    'id': user_id,
                    'name': 'Usuário Teste',
                    'email': 'teste@exemplo.com',
                    'created_at': datetime.now()
                }
                logger.info(f"Usando usuário simulado para ID: {user_id}")
            
            self.current_user = user
            logger.info(f"Login bem-sucedido para usuário ID: {user_id}")
            
            # Esconder tela de login
            if self.login_view:
                self.login_view.hide()
            
            # Limpar formulário
            self.login_view.clear_form()
            
            # Mostrar dashboard
            self.show_dashboard()
                
        except Exception as e:
            logger.error(f"Erro durante login: {e}")
    
    def handle_register_success(self, user_id: int):
        """Processa registro bem-sucedido"""
        try:
            logger.info(f"Usuário criado com sucesso: ID {user_id}")
            
            # Limpar formulário
            self.register_view.clear_form()
            
            # Voltar para tela de login
            self.show_login()
                
        except Exception as e:
            logger.error(f"Erro durante registro: {e}")
    
    def show_dashboard(self):
        """Mostra o dashboard principal"""
        if not self.dashboard_view:
            self.dashboard_view = DashboardView(self.current_user)
            # TODO: Conectar sinais do dashboard quando implementado
            # self.dashboard_view.logout_requested.connect(self.handle_logout)
            # self.dashboard_view.add_transaction_requested.connect(self.handle_add_transaction)
            # self.dashboard_view.view_transactions_requested.connect(self.handle_view_transactions)
            # self.dashboard_view.view_reports_requested.connect(self.handle_view_reports)
            # self.dashboard_view.view_settings_requested.connect(self.handle_view_settings)
        
        self.dashboard_view.show()
        self.dashboard_view.raise_()
        self.dashboard_view.activateWindow()
    
    def handle_logout(self):
        """Processa o logout do usuário"""
        try:
            logger.info(f"Logout do usuário: {self.current_user.get('email', 'Unknown')}")
            
            # Limpar dados da sessão
            self.current_user = None
            self.current_token = None
            
            # Fechar dashboard
            if self.dashboard_view:
                self.dashboard_view.close()
                self.dashboard_view = None
            
            # Mostrar tela de login
            self.show_login()
            
        except Exception as e:
            logger.error(f"Erro durante logout: {e}")
    
    def handle_add_transaction(self):
        """Processa a solicitação para adicionar transação"""
        # TODO: Implementar tela de adicionar transação
        logger.info("Solicitação para adicionar transação")
    
    def handle_view_transactions(self):
        """Processa a solicitação para visualizar transações"""
        # TODO: Implementar tela de transações
        logger.info("Solicitação para visualizar transações")
    
    def handle_view_reports(self):
        """Processa a solicitação para visualizar relatórios"""
        # TODO: Implementar tela de relatórios
        logger.info("Solicitação para visualizar relatórios")
    
    def handle_view_settings(self):
        """Processa a solicitação para visualizar configurações"""
        # TODO: Implementar tela de configurações
        logger.info("Solicitação para visualizar configurações")
    
    def is_authenticated(self) -> bool:
        """Verifica se o usuário está autenticado"""
        return self.current_user is not None and self.current_token is not None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Retorna os dados do usuário atual"""
        return self.current_user
    
    def get_current_token(self) -> Optional[str]:
        """Retorna o token atual"""
        return self.current_token
    
    def validate_token(self, token: str) -> bool:
        """Valida um token JWT"""
        try:
            user_id = self.user_model.validate_jwt_token(token)
            if user_id:
                # Verificar se o usuário ainda existe
                user = self.user_model.get_user_by_id(user_id)
                if user:
                    self.current_user = user
                    self.current_token = token
                    return True
            return False
        except Exception as e:
            logger.error(f"Erro ao validar token: {e}")
            return False 