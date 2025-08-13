import os
import sqlite3
import hashlib
import hmac
import secrets

# Caminho base do app
APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DB_PATH = os.path.join(APP_DIR, "financas.db")


class DatabaseManager:
    """Gerenciador de banco de dados SQLite simples e estável"""

    def __init__(self, db_path: str = None):
        # Garante DB dentro da pasta do app
        self.db_path = db_path or DEFAULT_DB_PATH
        self.init_database()

    def init_database(self):
        """Inicializa o banco de dados"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        senha TEXT NOT NULL,
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )'''
                )

                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS transacoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        descricao TEXT NOT NULL,
                        valor REAL NOT NULL,
                        tipo TEXT NOT NULL,
                        categoria TEXT NOT NULL,
                        data DATE NOT NULL,
                        usuario_id INTEGER,
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )'''
                )

                conn.commit()
        except Exception as e:
            print(f"Erro ao inicializar banco: {e}")

    # --- Senhas ---
    def _hash_password(self, senha: str) -> str:
        """Gera hash seguro (PBKDF2)"""
        iterations = 200_000
        salt = secrets.token_bytes(16)
        dk = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, iterations)
        return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"

    def _verify_password(self, senha: str, armazenado: str) -> bool:
        """Verifica hash; aceita legado em texto puro"""
        try:
            algo, iters, salt_hex, hash_hex = armazenado.split('$', 3)
            if algo != 'pbkdf2_sha256':
                return False
            iterations = int(iters)
            salt = bytes.fromhex(salt_hex)
            esperado = bytes.fromhex(hash_hex)
            calculado = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, iterations)
            return hmac.compare_digest(calculado, esperado)
        except Exception:
            return armazenado == senha

    # --- Usuários ---
    def inserir_usuario(self, nome, email, senha):
        """Insere usuário (com hash)"""
        try:
            senha_hash = self._hash_password(senha)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                    (nome, email, senha_hash),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            print("Email já existe")
            return False
        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")
            return False

    def verificar_login(self, email, senha):
        """Verifica credenciais (hash)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, nome, senha FROM usuarios WHERE email = ?",
                    (email,),
                )
                row = cursor.fetchone()
                if not row:
                    return None
                user_id, nome, senha_armazenada = row
                if self._verify_password(senha, senha_armazenada):
                    return (user_id, nome)
                return None
        except Exception as e:
            print(f"Erro ao verificar login: {e}")
            return None

    # --- Transações ---
    def inserir_transacao(self, descricao, valor, tipo, categoria, data, usuario_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO transacoes (descricao, valor, tipo, categoria, data, usuario_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (descricao, valor, tipo, categoria, data, usuario_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao inserir transação: {e}")
            return False

    def buscar_transacoes(self, usuario_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM transacoes WHERE usuario_id = ? ORDER BY data DESC",
                    (usuario_id,),
                )
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar transações: {e}")
            return []

    def atualizar_transacao(self, transacao_id, descricao, valor, tipo, categoria, data):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE transacoes
                    SET descricao = ?, valor = ?, tipo = ?, categoria = ?, data = ?
                    WHERE id = ?
                    """,
                    (descricao, valor, tipo, categoria, data, transacao_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar transação: {e}")
            return False

    def excluir_transacao(self, transacao_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transacoes WHERE id = ?", (transacao_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao excluir transação: {e}")
            return False


