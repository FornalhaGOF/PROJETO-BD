@echo off
taskkill /im mongod.exe /f >nul 2>&1
if errorlevel 1 (
  echo O MongoDB nao estava rodando.
) else (
  echo MongoDB encerrado.
)
