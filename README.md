# Sistema de Finanças Pessoais

Aplicação desktop em Python (PyQt5) com banco local SQLite.

## Instalação (Windows)
1. Execute `instalador.bat` (instala dependências e cria o banco).
2. Ao finalizar, o sistema será iniciado.

## Instalação manual
```bash
pip install -r requirements.txt
python app_desktop.py
```

## Uso
- Criar conta, fazer login, adicionar receitas/despesas.
- Aba Dashboard: visão geral (saldo, receitas, despesas).
- Aba Transações: lista completa, editar e excluir.
- Aba Nova Transação: formulário para adicionar.

## Estrutura
```
financas-nap1/
├── app_desktop.py        # Ponto de entrada
├── src/
│   ├── core/
│   │   └── db.py         # Banco e autenticação (hash PBKDF2)
│   └── ui/
│       ├── widgets.py    # Componentes básicos
│       ├── login.py      # Tela de login
│       ├── signup.py     # Tela de cadastro
│       └── dashboard.py  # Janela principal
├── instalador.bat        # Instalador
├── excluidor.bat         # Limpeza (remove DB e dependências)
├── requirements.txt      # Dependências (PyQt5)
└── README.md
```

## Observações
- Banco de dados: `financas.db` dentro da pasta do projeto.
- Senhas armazenadas com PBKDF2 (sha256) e salt.
- Para resetar e testar do zero: execute `excluidor.bat` e depois `instalador.bat`.