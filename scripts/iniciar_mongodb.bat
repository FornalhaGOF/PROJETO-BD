@echo off
setlocal
set "MONGOD=%LOCALAPPDATA%\mongodb-portable\mongodb-win32-x86_64-windows-8.0.3\bin\mongod.exe"
set "DADOS=%LOCALAPPDATA%\mongodb-data"

if not exist "%MONGOD%" (
  echo ERRO: mongod.exe nao encontrado em:
  echo %MONGOD%
  echo Baixe o MongoDB Community Server ^(ZIP^) e extraia nessa pasta.
  pause
  exit /b 1
)

if not exist "%DADOS%" mkdir "%DADOS%"

tasklist /fi "imagename eq mongod.exe" 2>nul | find /i "mongod.exe" >nul
if not errorlevel 1 (
  echo MongoDB ja esta rodando em 127.0.0.1:27017
  exit /b 0
)

echo Iniciando MongoDB...
start "MongoDB" /min "%MONGOD%" --dbpath "%DADOS%" --bind_ip 127.0.0.1 --port 27017 --logpath "%DADOS%\mongod.log" --logappend
timeout /t 4 >nul
echo MongoDB iniciado. Para encerrar use: scripts\parar_mongodb.bat
