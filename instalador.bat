@echo off
chcp 65001 >nul
title Instalador - Sistema de Finanças Pessoais

:: As senhas são armazenadas com PBKDF2 (sha256) dentro da aplicação

:: Ir para a pasta do script
cd /d "%~dp0"

echo.
echo ========================================
echo    SISTEMA DE FINANÇAS PESSOAIS
echo ========================================
echo.
echo Instalando dependências e configurando sistema...
echo.

:: Verificar se Python está instalado
echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo Por favor, instale Python 3.8+ de: https://python.org
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

:: Verificar versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python encontrado: %PYTHON_VERSION%
echo.

:: Verificar se pip está disponível
echo [2/4] Verificando pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: pip não encontrado!
    echo.
    echo Por favor, reinstale Python com pip habilitado
    echo.
    pause
    exit /b 1
)
echo ✅ pip encontrado
echo.

:: Instalar dependências
echo [3/4] Instalando dependências...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERRO: Falha ao instalar dependências!
    echo.
    pause
    exit /b 1
)
echo ✅ Dependências instaladas com sucesso!
echo.

:: Verificar se PyQt5 foi instalado
echo [4/4] Verificando instalação...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: PyQt5 não foi instalado corretamente!
    echo.
    echo Tentando instalação alternativa...
    python -m pip install PyQt5
    if errorlevel 1 (
        echo ❌ Falha na instalação alternativa!
        pause
        exit /b 1
    )
)

echo ✅ PyQt5 instalado com sucesso!
echo.

:: Criar banco de dados se não existir
echo [5/5] Configurando banco de dados...
if not exist "financas.db" (
    echo Criando banco de dados...
    python -c "import sqlite3; import os; db=r'%~dp0financas.db'; conn=sqlite3.connect(db); c=conn.cursor(); c.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, email TEXT UNIQUE NOT NULL, senha TEXT NOT NULL, data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'); c.execute('CREATE TABLE IF NOT EXISTS transacoes (id INTEGER PRIMARY KEY AUTOINCREMENT, descricao TEXT NOT NULL, valor REAL NOT NULL, tipo TEXT NOT NULL, categoria TEXT NOT NULL, data DATE NOT NULL, usuario_id INTEGER, data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'); conn.commit(); conn.close(); print('Banco de dados criado em:', db)"
    if errorlevel 1 (
        echo ❌ ERRO: Falha ao configurar banco de dados!
        pause
        exit /b 1
    )
) else (
    echo ✅ Banco de dados já existe em %~dp0financas.db
)

echo ✅ Banco de dados configurado!
echo.

:: Instalação concluída
echo ========================================
echo        INSTALAÇÃO CONCLUÍDA! 🎉
echo ========================================
echo.
echo ✅ Python verificado
echo ✅ Dependências instaladas
echo ✅ PyQt5 funcionando
echo ✅ Banco de dados configurado
echo.
echo Para executar o sistema:
echo   python app_desktop.py
echo.
echo Pressione qualquer tecla para executar o sistema...
pause >nul

:: Executar o sistema
echo.
echo 🚀 Iniciando Sistema de Finanças Pessoais...
echo.
python app_desktop.py

echo.
echo Sistema encerrado.
pause
