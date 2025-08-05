#!/usr/bin/env python3
"""
Script para Configurar Banco de Dados - Sistema de Finanças Pessoais
==================================================================

Este script cria o banco de dados e configura as permissões necessárias.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def setup_database():
    """Configura o banco de dados"""
    print("=" * 60)
    print("🗄️  Configuração do Banco de Dados")
    print("=" * 60)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Configurações de conexão (sem especificar banco)
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
    }
    
    try:
        # Conectar ao MySQL (sem especificar banco)
        print("🔌 Conectando ao MySQL...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Criar banco de dados
            db_name = os.getenv('DB_NAME', 'financas')
            print(f"📦 Criando banco de dados '{db_name}'...")
            
            create_db_query = f"""
            CREATE DATABASE IF NOT EXISTS {db_name} 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
            """
            
            cursor.execute(create_db_query)
            print(f"✅ Banco de dados '{db_name}' criado/verificado com sucesso")
            
            # Criar usuário se não existir
            user = os.getenv('DB_USER', 'finance_user')
            password = os.getenv('DB_PASSWORD', 'secure_password')
            
            if user != 'root':
                print(f"👤 Criando usuário '{user}'...")
                
                # Verificar se usuário existe
                cursor.execute("SELECT User FROM mysql.user WHERE User = %s", (user,))
                user_exists = cursor.fetchone()
                
                if not user_exists:
                    create_user_query = f"CREATE USER '{user}'@'localhost' IDENTIFIED BY '{password}'"
                    cursor.execute(create_user_query)
                    print(f"✅ Usuário '{user}' criado com sucesso")
                else:
                    print(f"✅ Usuário '{user}' já existe")
                
                # Conceder privilégios
                grant_query = f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{user}'@'localhost'"
                cursor.execute(grant_query)
                cursor.execute("FLUSH PRIVILEGES")
                print(f"✅ Privilégios concedidos para '{user}' no banco '{db_name}'")
            
            cursor.close()
            connection.close()
            
            print("\n🎉 Configuração do banco de dados concluída!")
            print(f"📋 Banco: {db_name}")
            print(f"👤 Usuário: {user}")
            print(f"🔗 Host: {config['host']}:{config['port']}")
            
            return True
            
    except Error as e:
        print(f"❌ Erro ao configurar banco de dados: {e}")
        print("\n💡 Verifique:")
        print("   1. Se o MySQL está rodando")
        print("   2. Se as credenciais no arquivo .env estão corretas")
        print("   3. Se você tem permissões de administrador")
        return False

def test_connection():
    """Testa a conexão com o banco configurado"""
    print("\n🧪 Testando conexão...")
    
    try:
        # Configurações incluindo o banco
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'finance_user'),
            'password': os.getenv('DB_PASSWORD', 'secure_password'),
            'database': os.getenv('DB_NAME', 'financas'),
        }
        
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ Conexão com banco de dados estabelecida!")
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ Erro ao testar conexão: {e}")
        return False

if __name__ == "__main__":
    if setup_database():
        test_connection()
    else:
        print("\n❌ Falha na configuração do banco de dados") 