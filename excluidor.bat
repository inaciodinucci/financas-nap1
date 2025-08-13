@echo off
chcp 65001 >nul
title Excluidor - Limpeza do Sistema de Finanças

:: Ir para a pasta do script
cd /d "%~dp0"

echo.
echo ========================================
echo        LIMPEZA DO SISTEMA
echo ========================================
echo.

echo Esta ação vai:
echo   - Apagar o banco de dados (financas.db) nesta pasta
echo   - Desinstalar dependências Python do projeto (PyQt5)
echo   - Limpar caches (__pycache__)
echo.
set /p CONFIRM="Tem certeza? (S/N): "
if /I not "%CONFIRM%"=="S" (
  echo Operacao cancelada.
  pause
  exit /b 0
)

Taskkill /IM python.exe /F >nul 2>&1

:: Remover banco de dados
if exist "%~dp0financas.db" (
  echo Removendo banco: %~dp0financas.db
  del /F /Q "%~dp0financas.db"
) else (
  echo Banco de dados não encontrado aqui.
)

:: Remover caches
if exist __pycache__ rmdir /S /Q __pycache__
for /r %%d in (__pycache__) do if exist "%%d" rmdir /S /Q "%%d"

:: Desinstalar dependências do projeto
python -m pip uninstall -y PyQt5 PyQt5-Qt5 PyQt5-sip >nul 2>&1

echo.
echo ✅ Limpeza concluída nesta pasta do projeto.
echo Agora execute: instalador.bat
pause
