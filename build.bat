@echo off

echo Limpando builds anteriores...
rmdir /s /q build
rmdir /s /q dist

echo Gerando o novo executavel...
pyinstaller --onefile --add-data ".env;." --name DNSManager dns_manager.py

echo.
echo Processo concluido! O novo .exe esta na pasta 'dist'.
pause