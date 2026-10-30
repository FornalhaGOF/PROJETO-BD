@echo off
setlocal
set "GIT=%LOCALAPPDATA%\PortableGit\bin\git.exe"
set "REPO_URL=%~1"

if "%REPO_URL%"=="" (
  echo Uso: scripts\publicar_github.bat https://github.com/SEU-USUARIO/SEU-REPO.git
  exit /b 1
)

if not exist "%GIT%" (
  echo Git nao encontrado em %GIT%
  echo Instale o Git for Windows ou ajuste o caminho neste arquivo.
  exit /b 1
)

cd /d "%~dp0.."
"%GIT%" remote remove origin >nul 2>&1
"%GIT%" remote add origin "%REPO_URL%"
"%GIT%" push -u origin main
if errorlevel 1 (
  echo.
  echo Falha no envio. Verifique se o repositorio existe, se e publico
  echo e se voce esta autenticado no GitHub.
) else (
  echo.
  echo Projeto publicado com sucesso.
)
