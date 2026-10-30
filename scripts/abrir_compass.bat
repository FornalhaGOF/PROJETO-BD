@echo off
setlocal
set "COMPASS="
for %%P in (
  "%LOCALAPPDATA%\MongoDB\Compass\MongoDBCompass.exe"
  "%LOCALAPPDATA%\Programs\MongoDB\Compass\MongoDBCompass.exe"
  "C:\Program Files\MongoDB\Compass\MongoDBCompass.exe"
) do if exist "%%~P" set "COMPASS=%%~P"

if not defined COMPASS (
  echo MongoDB Compass nao encontrado.
  echo Instale com: winget install --id MongoDB.Compass.Full
  pause
  exit /b 1
)

echo Abrindo o Compass em mongodb://localhost:27017 ...
start "" "%COMPASS%" "mongodb://localhost:27017"
