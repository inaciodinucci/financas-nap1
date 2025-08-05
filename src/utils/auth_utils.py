import re
import bcrypt
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class AuthUtils:
    """Utilitários para autenticação e validação"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Valida formato de email"""
        if not email:
            return False, "Email é obrigatório"
        
        # Padrão básico de email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Formato de email inválido"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Valida força da senha"""
        if not password:
            return False, "Senha é obrigatória"
        
        if len(password) < 8:
            return False, "Senha deve ter pelo menos 8 caracteres"
        
        if len(password) > 50:
            return False, "Senha deve ter no máximo 50 caracteres"
        
        # Verificar se contém pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', password):
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        
        # Verificar se contém pelo menos uma letra minúscula
        if not re.search(r'[a-z]', password):
            return False, "Senha deve conter pelo menos uma letra minúscula"
        
        # Verificar se contém pelo menos um número
        if not re.search(r'\d', password):
            return False, "Senha deve conter pelo menos um número"
        
        return True, ""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Valida nome do usuário"""
        if not name:
            return False, "Nome é obrigatório"
        
        if len(name.strip()) < 2:
            return False, "Nome deve ter pelo menos 2 caracteres"
        
        if len(name) > 100:
            return False, "Nome deve ter no máximo 100 caracteres"
        
        # Verificar se contém apenas letras, espaços e caracteres especiais comuns
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\'-]+$', name):
            return False, "Nome contém caracteres inválidos"
        
        return True, ""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Gera hash da senha"""
        try:
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            return password_hash.decode('utf-8')
        except Exception as e:
            logger.error(f"Erro ao gerar hash da senha: {e}")
            raise
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verifica se a senha está correta"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Erro ao verificar senha: {e}")
            return False
    
    @staticmethod
    def get_password_strength(password: str) -> Tuple[int, str]:
        """Calcula a força da senha (0-100)"""
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 20
        else:
            feedback.append("Adicione pelo menos 8 caracteres")
        
        if re.search(r'[A-Z]', password):
            score += 20
        else:
            feedback.append("Adicione letras maiúsculas")
        
        if re.search(r'[a-z]', password):
            score += 20
        else:
            feedback.append("Adicione letras minúsculas")
        
        if re.search(r'\d', password):
            score += 20
        else:
            feedback.append("Adicione números")
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 20
        else:
            feedback.append("Adicione caracteres especiais")
        
        # Classificação
        if score >= 80:
            strength = "Forte"
        elif score >= 60:
            strength = "Média"
        elif score >= 40:
            strength = "Fraca"
        else:
            strength = "Muito fraca"
        
        return score, strength
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Remove caracteres perigosos do input"""
        if not text:
            return ""
        
        # Remove caracteres de controle e HTML
        sanitized = re.sub(r'[<>&"\']', '', text)
        return sanitized.strip()
    
    @staticmethod
    def validate_amount(amount: str) -> Tuple[bool, str, Optional[float]]:
        """Valida valor monetário"""
        if not amount:
            return False, "Valor é obrigatório", None
        
        try:
            # Remove espaços e substitui vírgula por ponto
            clean_amount = amount.strip().replace(',', '.')
            
            # Verifica se é um número válido
            value = float(clean_amount)
            
            if value <= 0:
                return False, "Valor deve ser maior que zero", None
            
            if value > 999999999.99:
                return False, "Valor muito alto", None
            
            return True, "", value
        except ValueError:
            return False, "Valor inválido", None 