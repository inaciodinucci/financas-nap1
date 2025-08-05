#!/usr/bin/env python3
"""
Script de Setup - Sistema de Gestão de Finanças Pessoais
=======================================================

Este script automatiza o processo de instalação e configuração do sistema.
"""

import os
import sys
import subprocess
import platform
import pkg_resources
from pathlib import Path

class Instalador:
    """Classe para instalação e configuração do sistema"""
    
    def __init__(self):
        self.dependencies = {
            'PyQt5': '5.15.7',
            'mysql-connector-python': '8.0.28',
            'python-dotenv': '0.19.2',
            'bcrypt': '3.2.0',
            'pandas': '2.0.0',
            'matplotlib': '3.7.0',
            'PyJWT': '2.3.0',
            'openpyxl': '3.0.9'
        }
        self.skip_mysql_check = False
    
    def print_banner(self):
        """Exibe o banner do sistema"""
        print("=" * 60)
        print("💰 Sistema de Gestão de Finanças Pessoais")
        print("=" * 60)
        print("Instalador Automatizado")
        print("=" * 60)
        
        # Mostrar opções de linha de comando
        if len(sys.argv) > 1:
            print("\n📋 Opções detectadas:")
            for arg in sys.argv[1:]:
                if arg.startswith('--'):
                    print(f"   • {arg}")
        else:
            print("\n💡 Dica: Use --skip-mysql para pular a verificação do MySQL")
    
    def check_python_version(self):
        """Verifica a versão do Python"""
        print("🔍 Verificando versão do Python...")
        
        if sys.version_info < (3, 8):
            print("❌ Erro: Python 3.8 ou superior é necessário")
            print(f"   Versão atual: {sys.version}")
            return False
        
        print(f"✅ Python {sys.version.split()[0]} - OK")
        
        # Verificar se é Windows e mostrar dicas
        if platform.system() == "Windows":
            print("   💡 Dica: No Windows, alguns pacotes podem precisar de compiladores")
            print("   💡 Se houver problemas, tente instalar o Visual C++ Build Tools")
        
        return True
    
    def get_installed_packages(self):
        """Retorna um dicionário com pacotes instalados e suas versões"""
        installed = {}
        for dist in pkg_resources.working_set:
            installed[dist.project_name] = dist.version
        return installed
    
    def check_dependency(self, package_name, required_version):
        """Verifica se uma dependência está instalada na versão correta"""
        try:
            installed_version = pkg_resources.get_distribution(package_name).version
            return installed_version == required_version
        except pkg_resources.DistributionNotFound:
            return False
    
    def update_pip(self):
        """Atualiza o pip para a versão mais recente"""
        print("   🔄 Atualizando pip...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                          capture_output=True, text=True)
            print("   ✅ Pip atualizado")
            return True
        except Exception as e:
            print(f"   ⚠️  Não foi possível atualizar pip: {e}")
            return True  # Continua mesmo se falhar
    
    def install_dependencies(self):
        """Instala apenas as dependências que faltam"""
        print("\n📦 Verificando e instalando dependências...")
        
        try:
            # Verificar se pip está disponível
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                          check=True, capture_output=True)
            
            # Atualizar pip primeiro
            self.update_pip()
            
            installed_packages = self.get_installed_packages()
            packages_to_install = []
            
            # Verificar cada dependência
            for package, version in self.dependencies.items():
                if self.check_dependency(package, version):
                    print(f"   ✅ {package} {version} - Já instalado")
                else:
                    print(f"   ⏳ {package} {version} - Será instalado")
                    packages_to_install.append(f"{package}=={version}")
            
            # Instalar pacotes que faltam
            if packages_to_install:
                print(f"\n   📥 Instalando {len(packages_to_install)} dependência(s)...")
                
                for package_spec in packages_to_install:
                    print(f"      Instalando {package_spec}...")
                    try:
                        # Tentar instalar com --user para evitar problemas de permissão
                        result = subprocess.run(
                            [sys.executable, "-m", "pip", "install", "--user", package_spec], 
                            capture_output=True, text=True
                        )
                        
                        if result.returncode == 0:
                            print(f"      ✅ {package_spec} instalado com sucesso")
                        else:
                            # Se falhar com --user, tentar sem
                            print(f"      ⚠️  Tentando instalação alternativa para {package_spec}...")
                            result = subprocess.run(
                                [sys.executable, "-m", "pip", "install", package_spec], 
                                capture_output=True, text=True
                            )
                            
                            if result.returncode == 0:
                                print(f"      ✅ {package_spec} instalado com sucesso")
                            else:
                                print(f"      ❌ Erro ao instalar {package_spec}")
                                print(f"         Erro: {result.stderr}")
                                
                                # Para pandas, tentar versão mais recente
                                if package_spec.startswith("pandas=="):
                                    print(f"      🔄 Tentando versão mais recente do pandas...")
                                    
                                    # Tentar diferentes abordagens para pandas
                                    pandas_attempts = [
                                        ["pandas"],
                                        ["pandas", "--no-deps"],
                                        ["pandas", "--only-binary=all"],
                                        ["pandas", "--prefer-binary"]
                                    ]
                                    
                                    pandas_installed = False
                                    for attempt in pandas_attempts:
                                        print(f"         Tentativa: pip install {' '.join(attempt)}")
                                        result = subprocess.run(
                                            [sys.executable, "-m", "pip", "install"] + attempt, 
                                            capture_output=True, text=True
                                        )
                                        if result.returncode == 0:
                                            print(f"      ✅ pandas instalado com sucesso")
                                            pandas_installed = True
                                            break
                                        else:
                                            print(f"         Falhou: {result.stderr[:100]}...")
                                    
                                    if not pandas_installed:
                                        print(f"      ❌ Falha ao instalar pandas após múltiplas tentativas")
                                        print(f"      💡 Tente instalar manualmente: pip install pandas")
                                        return False
                                else:
                                    return False
                                    
                    except Exception as e:
                        print(f"      ❌ Erro inesperado ao instalar {package_spec}: {e}")
                        return False
            else:
                print("   🎉 Todas as dependências já estão instaladas!")
            
            print("✅ Verificação de dependências concluída")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao verificar pip: {e}")
            return False
        except FileNotFoundError:
            print("❌ Erro: pip não encontrado")
            return False
    
    def create_env_file(self):
        """Cria o arquivo de configuração .env"""
        print("\n⚙️  Configurando variáveis de ambiente...")
        
        env_file = Path(".env")
        env_example = Path("env.example")
        
        if env_file.exists():
            print("   Arquivo .env já existe")
            return True
        
        if not env_example.exists():
            print("❌ Arquivo env.example não encontrado")
            return False
        
        try:
            # Copiar arquivo de exemplo
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Arquivo .env criado com sucesso")
            print("   ⚠️  IMPORTANTE: Edite o arquivo .env com suas configurações")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar arquivo .env: {e}")
            return False
    
    def check_mysql(self):
        """Verifica se o MySQL está disponível"""
        print("\n🗄️  Verificando MySQL...")
        
        try:
            # Tentar conectar ao MySQL
            import mysql.connector
            from dotenv import load_dotenv
            
            load_dotenv()
            
            config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', 3306)),
                'user': os.getenv('DB_USER', 'finance_user'),
                'password': os.getenv('DB_PASSWORD', 'secure_password'),
                'database': os.getenv('DB_NAME', 'financas'),
            }
            
            connection = mysql.connector.connect(**config)
            connection.close()
            
            print("✅ Conexão com MySQL estabelecida")
            return True
            
        except ImportError:
            print("❌ mysql-connector-python não instalado")
            return False
        except Exception as e:
            print(f"❌ Erro ao conectar com MySQL: {e}")
            print("   Verifique se:")
            print("   1. MySQL está rodando")
            print("   2. As configurações no .env estão corretas")
            print("   3. O banco de dados existe")
            return False
    
    def create_database_schema(self):
        """Cria o esquema do banco de dados"""
        print("\n🏗️  Criando esquema do banco de dados...")
        
        try:
            from src.models.database import db_manager
            
            if db_manager.create_tables():
                print("✅ Tabelas criadas com sucesso")
                return True
            else:
                print("❌ Erro ao criar tabelas")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao criar esquema: {e}")
            return False
    
    def test_application(self):
        """Testa se a aplicação pode ser executada"""
        print("\n🧪 Testando aplicação...")
        
        try:
            # Importar módulos principais
            from src.models.database import db_manager
            from src.controllers.auth_controller import AuthController
            
            print("✅ Módulos importados com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao testar aplicação: {e}")
            return False
    
    def show_troubleshooting_tips(self):
        """Mostra dicas de solução de problemas"""
        print("\n🔧 Dicas de Solução de Problemas:")
        print("=" * 50)
        
        if platform.system() == "Windows":
            print("🪟 Windows:")
            print("   • Instale o Visual C++ Build Tools se houver erros de compilação")
            print("   • Use 'pip install --user' para evitar problemas de permissão")
            print("   • Considere usar Anaconda para pacotes científicos")
        
        print("🐍 Python:")
        print("   • Certifique-se de usar Python 3.8+")
        print("   • Use ambiente virtual: python -m venv venv")
        print("   • Atualize pip: python -m pip install --upgrade pip")
        
        print("📦 Dependências:")
        print("   • pandas: Pode precisar de versão mais recente")
        print("   • matplotlib: Verifique se há conflitos de versão")
        print("   • PyQt5: Pode precisar de dependências do sistema")
        
        print("🗄️ MySQL:")
        print("   • Verifique se o MySQL está rodando")
        print("   • Confirme as credenciais no arquivo .env")
        print("   • Teste a conexão manualmente")
    
    def show_next_steps(self):
        """Mostra os próximos passos"""
        print("\n" + "=" * 60)
        print("🎉 Instalação Concluída!")
        print("=" * 60)
        print("\n📋 Próximos Passos:")
        print("1. Configure o arquivo .env com suas credenciais do MySQL")
        print("2. Execute: python main.py")
        print("3. Crie sua conta no sistema")
        print("4. Explore o dashboard!")
        print("\n📚 Documentação:")
        print("- README.md: Guia completo")
        print("- env.example: Modelo de configuração")
        print("\n🐛 Problemas?")
        print("- Verifique os logs em financas_pessoais.log")
        print("- Consulte a seção de solução de problemas no README")
        
        # Mostrar dicas específicas se houver problemas
        self.show_troubleshooting_tips()
        
        print("\n" + "=" * 60)
    
    def run(self):
        """Executa o processo completo de instalação"""
        self.print_banner()
        
        # Verificar argumentos de linha de comando
        if len(sys.argv) > 1:
            if '--skip-mysql' in sys.argv or '--no-mysql' in sys.argv:
                self.skip_mysql_check = True
                print("   ⏭️  Verificação do MySQL será pulada (argumento --skip-mysql)")
        
        # Verificar Python
        if not self.check_python_version():
            return False
        
        # Instalar dependências
        if not self.install_dependencies():
            print("\n❌ Falha na instalação das dependências")
            return False
        
        # Criar arquivo .env
        if not self.create_env_file():
            print("\n❌ Falha na criação do arquivo .env")
            return False
        
        # Verificar MySQL (opcional)
        if not self.skip_mysql_check:
            print("\n⚠️  Verificação do MySQL (opcional)")
            print("   Se você ainda não configurou o MySQL, pode pular esta etapa")
            print("   Pressione Ctrl+C para pular ou aguarde 10 segundos...")
            
            try:
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError("Timeout - pulando verificação do MySQL")
                
                # Configurar timeout de 10 segundos
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                
                response = input("   Deseja verificar a conexão com MySQL? (s/n): ").lower()
                signal.alarm(0)  # Cancelar alarme
                
                if response in ['s', 'sim', 'y', 'yes']:
                    if not self.check_mysql():
                        print("\n⚠️  MySQL não está configurado corretamente")
                        print("   Configure o arquivo .env e tente novamente")
                    else:
                        # Criar esquema do banco
                        if not self.create_database_schema():
                            print("\n❌ Falha na criação do esquema do banco")
                            return False
                else:
                    print("   ⏭️  Verificação do MySQL pulada")
                    
            except (KeyboardInterrupt, TimeoutError):
                print("\n   ⏭️  Verificação do MySQL pulada (timeout/interrupção)")
            except Exception as e:
                print(f"\n   ⚠️  Erro na verificação do MySQL: {e}")
                print("   ⏭️  Continuando sem verificação...")
        else:
            print("\n   ⏭️  Verificação do MySQL pulada (configurado)")
        
        # Testar aplicação
        if not self.test_application():
            print("\n❌ Falha no teste da aplicação")
            return False
        
        # Mostrar próximos passos
        self.show_next_steps()
        return True

def show_help():
    """Mostra a ajuda do script"""
    print("=" * 60)
    print("💰 Sistema de Gestão de Finanças Pessoais - Instalador")
    print("=" * 60)
    print("\n📋 Uso:")
    print("   python setup.py [opções]")
    print("\n🔧 Opções:")
    print("   --help, -h          Mostra esta ajuda")
    print("   --skip-mysql        Pula a verificação do MySQL")
    print("   --no-mysql          Pula a verificação do MySQL")
    print("\n💡 Exemplos:")
    print("   python setup.py                    # Instalação normal")
    print("   python setup.py --skip-mysql       # Pula verificação MySQL")
    print("   python setup.py --help             # Mostra ajuda")
    print("\n" + "=" * 60)

def main():
    """Função principal do script"""
    # Verificar se o usuário quer ajuda
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        return
    
    try:
        instalador = Instalador()
        success = instalador.run()
        
        if not success:
            print("\n❌ Instalação falhou. Verifique os erros acima.")
            sys.exit(1)
        else:
            print("\n🎉 Instalação concluída com sucesso!")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalação interrompida pelo usuário.")
        print("💡 Para continuar mais tarde, execute: python setup.py")
        print("💡 Para pular MySQL: python setup.py --skip-mysql")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Verifique se você tem permissões adequadas e tente novamente.")
        sys.exit(1)

if __name__ == "__main__":
    main() 