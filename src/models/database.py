import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de conexão com o banco de dados MySQL"""
    
    def __init__(self):
        load_dotenv()
        self.connection = None
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'finance_user'),
            'password': os.getenv('DB_PASSWORD', 'secure_password'),
            'database': os.getenv('DB_NAME', 'personal_finance'),
            'charset': 'utf8mb4',
            'autocommit': True
        }
    
    def connect(self) -> bool:
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                logger.info("Conexão com MySQL estabelecida com sucesso")
                return True
        except Error as e:
            logger.error(f"Erro ao conectar com MySQL: {e}")
            return False
        return False
    
    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexão com MySQL fechada")
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[list]:
        """Executa uma consulta SELECT"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            logger.error(f"Erro ao executar query: {e}")
            return None
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Executa uma operação INSERT, UPDATE ou DELETE"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return False
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            cursor.close()
            return True
        except Error as e:
            logger.error(f"Erro ao executar update: {e}")
            return False
    
    def get_last_insert_id(self) -> Optional[int]:
        """Retorna o ID do último registro inserido"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except Error as e:
            logger.error(f"Erro ao obter último ID: {e}")
            return None
    
    def create_tables(self) -> bool:
        """Cria as tabelas do banco de dados se não existirem"""
        tables = {
            'users': """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """,
            'categories': """
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    color VARCHAR(7) DEFAULT '#3498db',
                    icon VARCHAR(20),
                    is_default BOOLEAN DEFAULT false,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """,
            'transactions': """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    category_id INT,
                    amount DECIMAL(10, 2) NOT NULL,
                    type ENUM('income', 'expense') NOT NULL,
                    date DATE NOT NULL,
                    description VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
                )
            """,
            'user_settings': """
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INT PRIMARY KEY,
                    currency VARCHAR(3) DEFAULT 'BRL',
                    language VARCHAR(5) DEFAULT 'pt-BR',
                    start_week_on ENUM('sunday', 'monday') DEFAULT 'sunday',
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """
        }
        
        try:
            for table_name, create_sql in tables.items():
                if not self.execute_update(create_sql):
                    logger.error(f"Erro ao criar tabela {table_name}")
                    return False
                logger.info(f"Tabela {table_name} criada/verificada com sucesso")
            return True
        except Error as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            return False

# Instância global do gerenciador de banco
db_manager = DatabaseManager() 