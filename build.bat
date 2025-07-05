@echo off
title Construtor do DNSManager


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


echo Gerando o novo executavel...


pyinstaller DNSManager.spec


if %errorlevel% neq 0 (
    echo.
    echo Ocorreu um erro durante a compilacao com o PyInstaller.
    pause
    exit /b %errorlevel%
)


echo.
echo =======================================================
echo.
echo  Processo concluido com sucesso!
echo  O novo executavel (DNSManager.exe) esta na pasta 'dist'.
echo.
echo =======================================================
echo.
pause