# 💰 Sistema de Gestão de Finanças Pessoais

Uma aplicação desktop completa para controle financeiro pessoal desenvolvida com **PyQt5** e **MySQL**.

## 🚀 Funcionalidades

### ✅ Implementadas
- **Autenticação Segura**: Login e registro com validação JWT
- **Dashboard Intuitivo**: Visão geral com gráficos e resumos
- **Gestão de Transações**: CRUD completo de transações
- **Análise Visual**: Gráficos de pizza e linha com Matplotlib
- **Filtros Avançados**: Por período, categoria e tipo
- **Design Hook**: Interface moderna baseada no tema Hook
- **Gradiente Elegante**: Fundo com gradiente preto sofisticado
- **Cards Brancos**: Formulários em cards brancos com bordas suaves
- **Tipografia Muli**: Fonte moderna e legível
- **Cores Índigo**: Paleta de cores elegante e profissional

### 🔄 Em Desenvolvimento
- Relatórios detalhados
- Exportação de dados (CSV/Excel)
- Configurações do usuário
- Categorias customizáveis

## 📋 Pré-requisitos

### Software Necessário
- **Python 3.8+**
- **MySQL 8.0+**
- **Git** (para clonar o repositório)

### Sistema Operacional
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Ubuntu 18.04+ / Debian 10+

## 🛠️ Instalação

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd financas-pessoais
```

### 2. Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados

#### 4.1. Instalar MySQL
- **Windows**: Baixar e instalar MySQL Installer
- **macOS**: `brew install mysql`
- **Ubuntu**: `sudo apt install mysql-server`

#### 4.2. Criar Banco de Dados
```sql
CREATE DATABASE financas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 4.3. Criar Usuário
```sql
CREATE USER 'finance_user'@'localhost' IDENTIFIED BY 'sua_senha_segura';
GRANT ALL PRIVILEGES ON financas.* TO 'finance_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo:
```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:
```ini
# Configurações de Banco de Dados
DB_HOST=localhost
DB_PORT=3306
DB_USER=finance_user
DB_PASSWORD=sua_senha_segura
DB_NAME=financas

# Configurações de Segurança
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
JWT_EXPIRE_HOURS=24
```

## 🚀 Executando a Aplicação

### Iniciar o Sistema
```bash
python main.py
```

### Testar Interface (Design Hook)
```bash
# Testar ambas as views
python test_ui.py

# Testar apenas login
python test_ui.py login

# Testar apenas registro
python test_ui.py register
```

### Primeiro Acesso
1. Clique em "Cadastre-se" na tela de login
2. Preencha seus dados pessoais
3. Faça login com suas credenciais
4. Explore o dashboard!

## 📁 Estrutura do Projeto

```
financas_pessoais/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── env.example            # Modelo de configuração
├── README.md              # Documentação
├── src/
│   ├── controllers/       # Lógica de negócios
│   │   └── auth_controller.py
│   ├── models/            # Modelos de dados
│   │   ├── database.py
│   │   ├── user_model.py
│   │   └── transaction_model.py
│   ├── views/             # Interfaces gráficas
│   │   ├── auth/
│   │   │   ├── login_view.py
│   │   │   └── register_view.py
│   │   └── dashboard_view.py
│   ├── utils/             # Utilitários
│   │   ├── auth_utils.py
│   │   └── date_utils.py
│   └── widgets/           # Componentes reutilizáveis
│       ├── pie_chart.py
│       └── date_filter.py
└── tests/                 # Testes (futuro)
```

## 🎯 Funcionalidades Principais

### 🔐 Autenticação
- **Registro**: Validação de email e força de senha
- **Login**: Autenticação segura com JWT
- **Recuperação**: Sistema de recuperação de senha (futuro)

### 📊 Dashboard
- **Saldo Atual**: Visão geral do saldo
- **Receitas vs Despesas**: Comparativo mensal
- **Gráfico de Categorias**: Distribuição por categoria
- **Evolução Temporal**: Gráfico de linha mensal
- **Transações Recentes**: Lista das últimas transações

### 💳 Transações
- **Adicionar**: Nova transação com categoria
- **Editar**: Modificar transações existentes
- **Excluir**: Remover transações
- **Filtrar**: Por período, categoria e tipo

### 📈 Análises
- **Gráficos Interativos**: Matplotlib integrado
- **Filtros Avançados**: Múltiplos critérios
- **Exportação**: CSV e Excel (futuro)

## 🎨 Interface

### Design Principles
- **Minimalista**: Interface limpa e focada
- **Responsiva**: Adaptável a diferentes resoluções
- **Acessível**: Cores e contrastes adequados
- **Intuitiva**: Navegação clara e lógica
- **Design Hook**: Baseado no tema Hook moderno e elegante
- **Gradiente Sofisticado**: Fundo com gradiente preto elegante
- **Cards Modernos**: Formulários em cards brancos com bordas suaves
- **Tipografia Elegante**: Fonte Muli para melhor legibilidade
- **Paleta Índigo**: Cores profissionais e modernas

### Componentes
- **Cards Informativos**: Resumos visuais
- **Gráficos Interativos**: Tooltips e animações
- **Formulários Validados**: Feedback em tempo real
- **Navegação Intuitiva**: Menus e botões claros

## 🔧 Configuração Avançada

### Personalização de Cores
Edite os arquivos de estilo nos componentes para personalizar cores:
```python
# Exemplo de personalização
self.setStyleSheet("""
    QWidget {
        background-color: #f8f9fa;
        color: #2c3e50;
    }
""")
```

### Configuração de Banco
Para usar outro banco de dados, modifique `src/models/database.py`:
```python
# Exemplo para PostgreSQL
import psycopg2
# Adaptar queries SQL conforme necessário
```

## 🐛 Solução de Problemas

### Erro de Conexão com MySQL
```
Erro: Falha ao conectar com o banco de dados
```
**Solução:**
1. Verifique se o MySQL está rodando
2. Confirme as credenciais no arquivo `.env`
3. Teste a conexão manualmente:
```bash
mysql -u finance_user -p personal_finance
```

### Erro de Dependências
```
ModuleNotFoundError: No module named 'PyQt5'
```
**Solução:**
```bash
pip install PyQt5
# ou
pip install -r requirements.txt
```

### Erro de Permissões
```
Access denied for user 'finance_user'@'localhost'
```
**Solução:**
```sql
GRANT ALL PRIVILEGES ON personal_finance.* TO 'finance_user'@'localhost';
FLUSH PRIVILEGES;
```

## 📝 Logs

A aplicação gera logs detalhados em:
- **Arquivo**: `financas_pessoais.log`
- **Console**: Saída em tempo real
- **Nível**: INFO, WARNING, ERROR

### Exemplo de Log
```
2023-12-15 10:30:15 - src.models.database - INFO - Conexão com MySQL estabelecida com sucesso
2023-12-15 10:30:16 - src.controllers.auth_controller - INFO - Login bem-sucedido para usuario@email.com
```

## 🔒 Segurança

### Implementado
- **Hash de Senhas**: bcrypt com salt
- **JWT Tokens**: Autenticação stateless
- **Validação de Input**: Sanitização de dados
- **Prepared Statements**: Prevenção de SQL Injection

### Recomendações
- Use senhas fortes
- Mantenha o sistema atualizado
- Configure firewall adequadamente
- Faça backups regulares

## 🚀 Roadmap

### Versão 1.1 (Próxima)
- [ ] Relatórios detalhados
- [ ] Exportação CSV/Excel
- [ ] Categorias customizáveis
- [ ] Configurações do usuário

### Versão 1.2 (Futuro)
- [ ] Backup automático
- [ ] Notificações
- [ ] Temas (claro/escuro)
- [ ] Multi-idioma

### Versão 2.0 (Longo Prazo)
- [ ] Versão web
- [ ] App mobile
- [ ] Integração bancária
- [ ] IA para categorização

## 🤝 Contribuindo

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Padrões de Código
- **PEP 8**: Estilo Python
- **Type Hints**: Tipagem explícita
- **Docstrings**: Documentação clara
- **Logging**: Logs informativos

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Sistema de Finanças Pessoais**
- **Versão**: 1.0.0
- **Data**: Dezembro 2023

## 🙏 Agradecimentos

- **PyQt5**: Framework de interface
- **MySQL**: Banco de dados
- **Matplotlib**: Gráficos
- **Comunidade Python**: Suporte e recursos

---

**💡 Dica**: Para melhor experiência, execute a aplicação em tela cheia e explore todas as funcionalidades do dashboard! 