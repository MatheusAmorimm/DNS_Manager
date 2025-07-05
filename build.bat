@echo off
title Construtor do DNSManager

REM --- Limpeza dos builds anteriores ---
echo Limpando builds anteriores...
if exist "build" (
    rmdir /s /q "build"
    echo Pasta 'build' removida.
)
if exist "dist" (
    rmdir /s /q "dist"
    echo Pasta 'dist' removida.
)
echo.

REM --- Geracao do executavel usando o arquivo .spec ---
echo Gerando o novo executavel...
REM Usamos o arquivo .spec porque ele ja contem a lista de modulos (hiddenimports).
REM A opcao --onefile pode ser passada aqui para sobrescrever a configuracao do spec, se necessario.
pyinstaller --onefile DNSManager.spec

REM --- Verificacao de Erro ---
if %errorlevel% neq 0 (
    echo.
    echo Ocorreu um erro durante a compilacao com o PyInstaller.
    pause
    exit /b %errorlevel%
)

REM --- Mensagem de Conclusao ---
echo.
echo =======================================================
echo.
echo  Processo concluido com sucesso!
echo  O novo executavel (DNSManager.exe) esta na pasta 'dist'.
echo.
echo =======================================================
echo.
pause