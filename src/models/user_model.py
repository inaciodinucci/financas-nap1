from typing import Optional, Dict, Any
from ..models.database import db_manager
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class UserModel:
    """Modelo para gerenciamento de usuários"""
    
    def __init__(self):
        self.db = db_manager
    
    def create_user(self, name: str, email: str, password: str) -> Optional[int]:
        """Cria um novo usuário"""
        try:
            # Verificar se o email já existe
            existing_user = self.get_user_by_email(email)
            if existing_user:
                logger.warning(f"Email {email} já está em uso")
                return None
            
            # Hash da senha
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Inserir usuário
            query = """
                INSERT INTO users (name, email, password_hash)
                VALUES (%s, %s, %s)
            """
            if self.db.execute_update(query, (name, email, password_hash.decode('utf-8'))):
                user_id = self.db.get_last_insert_id()
                
                # Criar configurações padrão do usuário
                self._create_default_settings(user_id)
                self._create_default_categories(user_id)
                
                logger.info(f"Usuário {email} criado com sucesso")
                return user_id
            
            return None
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica um usuário"""
        try:
            user = self.get_user_by_email(email)
            if not user:
                return None
            
            # Verificar senha
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                # Gerar token JWT
                token = self._generate_jwt_token(user['id'])
                
                logger.info(f"Usuário {email} autenticado com sucesso")
                return {
                    'user': user,
                    'token': token
                }
            
            return None
        except Exception as e:
            logger.error(f"Erro ao autenticar usuário: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por email"""
        try:
            query = "SELECT * FROM users WHERE email = %s"
            result = self.db.execute_query(query, (email,))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por email: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca usuário por ID"""
        try:
            query = "SELECT * FROM users WHERE id = %s"
            result = self.db.execute_query(query, (user_id,))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por ID: {e}")
            return None
    
    def update_user_profile(self, user_id: int, name: str = None, email: str = None) -> bool:
        """Atualiza o perfil do usuário"""
        try:
            updates = []
            params = []
            
            if name:
                updates.append("name = %s")
                params.append(name)
            
            if email:
                # Verificar se o email já existe (exceto para o usuário atual)
                existing_user = self.get_user_by_email(email)
                if existing_user and existing_user['id'] != user_id:
                    logger.warning(f"Email {email} já está em uso")
                    return False
                
                updates.append("email = %s")
                params.append(email)
            
            if not updates:
                return True
            
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            
            success = self.db.execute_update(query, tuple(params))
            if success:
                logger.info(f"Perfil do usuário {user_id} atualizado com sucesso")
            
            return success
        except Exception as e:
            logger.error(f"Erro ao atualizar perfil do usuário: {e}")
            return False
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Altera a senha do usuário"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False
            
            # Verificar senha atual
            if not bcrypt.checkpw(current_password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                logger.warning(f"Senha atual incorreta para usuário {user_id}")
                return False
            
            # Hash da nova senha
            new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            
            # Atualizar senha
            query = "UPDATE users SET password_hash = %s WHERE id = %s"
            success = self.db.execute_update(query, (new_password_hash.decode('utf-8'), user_id))
            
            if success:
                logger.info(f"Senha do usuário {user_id} alterada com sucesso")
            
            return success
        except Exception as e:
            logger.error(f"Erro ao alterar senha: {e}")
            return False
    
    def validate_jwt_token(self, token: str) -> Optional[int]:
        """Valida um token JWT e retorna o user_id"""
        try:
            secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload.get('user_id')
        except jwt.ExpiredSignatureError:
            logger.warning("Token JWT expirado")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token JWT inválido: {e}")
            return None
    
    def _generate_jwt_token(self, user_id: int) -> str:
        """Gera um token JWT para o usuário"""
        try:
            secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
            expire_hours = int(os.getenv('JWT_EXPIRE_HOURS', 24))
            
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(hours=expire_hours),
                'iat': datetime.utcnow()
            }
            
            return jwt.encode(payload, secret_key, algorithm='HS256')
        except Exception as e:
            logger.error(f"Erro ao gerar token JWT: {e}")
            return ""
    
    def _create_default_settings(self, user_id: int):
        """Cria configurações padrão para o usuário"""
        try:
            query = """
                INSERT INTO user_settings (user_id, currency, language, start_week_on)
                VALUES (%s, %s, %s, %s)
            """
            self.db.execute_update(query, (user_id, 'BRL', 'pt-BR', 'sunday'))
        except Exception as e:
            logger.error(f"Erro ao criar configurações padrão: {e}")
    
    def _create_default_categories(self, user_id: int):
        """Cria categorias padrão para o usuário"""
        try:
            default_categories = [
                ('Alimentação', '#e74c3c', '🍽️'),
                ('Transporte', '#3498db', '🚗'),
                ('Moradia', '#2ecc71', '🏠'),
                ('Saúde', '#9b59b6', '🏥'),
                ('Educação', '#f39c12', '📚'),
                ('Lazer', '#1abc9c', '🎮'),
                ('Vestuário', '#e67e22', '👕'),
                ('Salário', '#27ae60', '💰'),
                ('Freelance', '#f1c40f', '💼'),
                ('Investimentos', '#8e44ad', '📈')
            ]
            
            for name, color, icon in default_categories:
                query = """
                    INSERT INTO categories (user_id, name, color, icon, is_default)
                    VALUES (%s, %s, %s, %s, %s)
                """
                is_default = name in ['Salário', 'Freelance', 'Investimentos']
                self.db.execute_update(query, (user_id, name, color, icon, is_default))
        except Exception as e:
            logger.error(f"Erro ao criar categorias padrão: {e}") 