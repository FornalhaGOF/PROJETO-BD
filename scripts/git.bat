@echo off
rem Atalho para o Git portatil (nao precisa estar no PATH do Windows).
rem Exemplos:
rem   scripts\git.bat status
rem   scripts\git.bat add .
rem   scripts\git.bat commit -m "minha alteracao"
rem   scripts\git.bat push
setlocal
set "GIT=%LOCALAPPDATA%\PortableGit\bin\git.exe"
if not exist "%GIT%" (
  echo Git portatil nao encontrado em:
  echo   %GIT%
  echo Instale o Git for Windows ou ajuste o caminho neste arquivo.
  exit /b 1
)
cd /d "%~dp0.."
"%GIT%" %*
