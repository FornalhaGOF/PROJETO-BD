@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
set "PYTHONIOENCODING=utf-8"
title Demonstracao - Projeto 10 Dashboard de Vendas
cd /d "%~dp0.."

rem ------------------------------------------------------------------
rem  Uso normal:  scripts\demo_apresentacao.bat
rem  Ensaio:      scripts\demo_apresentacao.bat auto   (sem pausas)
rem ------------------------------------------------------------------
set "PAUSA=1"
if /i "%~1"=="auto" set "PAUSA="

set "PY=.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [ERRO] Ambiente virtual nao encontrado.
  echo Execute: python -m venv .venv
  echo           .venv\Scripts\python.exe -m pip install -r requirements.txt
  if defined PAUSA pause
  exit /b 1
)

echo ============================================================
echo   PROJETO 10 - DASHBOARD DE VENDAS (MongoDB + Python)
echo   Demonstracao guiada - pressione ENTER para cada etapa
echo ============================================================
echo.
if defined PAUSA pause

rem ---------------------------------------------------------------- 0
echo [0/4] Ligando o MongoDB local...
call "%~dp0iniciar_mongodb.bat"
echo.
if defined PAUSA pause

rem ---------------------------------------------------------------- 1
cls
echo [1/4] VERIFICANDO O AMBIENTE
echo ------------------------------------------------------------
"%PY%" verificar_ambiente.py
echo.
if defined PAUSA pause

rem ---------------------------------------------------------------- 2
cls
echo [2/4] RELATORIO DE VENDAS (aggregation pipeline)
echo ------------------------------------------------------------
echo Fale: "$match filtra, $group soma por categoria, $sort ordena."
echo.
"%PY%" -m p10_dashboard.main --reset
echo.
if defined PAUSA pause

rem ---------------------------------------------------------------- 3
cls
echo [3/4] RODANDO DE NOVO PARA PROVAR A IDEMPOTENCIA
echo ------------------------------------------------------------
echo Fale: "Os totais sao identicos porque o codigo da venda e unico."
echo.
"%PY%" -m p10_dashboard.main --sem-grafico --sem-csv
echo.
if defined PAUSA pause

rem ---------------------------------------------------------------- 4
cls
echo [4/4] FILTRO POR PERIODO (desafio extra)
echo ------------------------------------------------------------
"%PY%" -m p10_dashboard.main --dias 7 --top 3 --sem-grafico --sem-csv
echo.
if defined PAUSA pause

rem ---------------------------------------------------------------- 5
cls
echo [BONUS] TESTES AUTOMATIZADOS
echo ------------------------------------------------------------
"%PY%" -m unittest discover -s tests -t . -v
echo.
if defined PAUSA pause

rem ---------------------------------------------------------------- 6
cls
echo ABRINDO AS EVIDENCIAS
echo ------------------------------------------------------------
if exist "p10_dashboard\grafico_vendas.png" (
  echo Grafico: p10_dashboard\grafico_vendas.png
) else (
  echo [AVISO] grafico_vendas.png nao encontrado.
)
if exist "p10_dashboard\relatorio_vendas.csv" (
  echo CSV:     p10_dashboard\relatorio_vendas.csv
)
echo.
if not defined PAUSA goto :fim
start "" "p10_dashboard\grafico_vendas.png"

:fim
echo ============================================================
echo   Demonstracao concluida.
echo   Lembre de mostrar o repositorio PUBLICO no GitHub.
echo ============================================================
if defined PAUSA pause
