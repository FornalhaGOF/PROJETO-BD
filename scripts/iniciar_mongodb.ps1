# Inicia o MongoDB portatil (sem servico do Windows).
# Uso: powershell -ExecutionPolicy Bypass -File scripts\iniciar_mongodb.ps1
$ErrorActionPreference = 'Stop'

$mongod = Join-Path $env:LOCALAPPDATA 'mongodb-portable\mongodb-win32-x86_64-windows-8.0.3\bin\mongod.exe'
$dados = Join-Path $env:LOCALAPPDATA 'mongodb-data'

if (-not (Test-Path $mongod)) {
    Write-Host "ERRO: mongod.exe nao encontrado em:`n  $mongod"
    exit 1
}

if (-not (Test-Path $dados)) {
    New-Item -ItemType Directory -Path $dados | Out-Null
}

if (Get-Process mongod -ErrorAction SilentlyContinue) {
    Write-Host 'MongoDB ja esta rodando em 127.0.0.1:27017'
    exit 0
}

Start-Process -FilePath $mongod -WindowStyle Hidden -ArgumentList @(
    '--dbpath', "`"$dados`"",
    '--bind_ip', '127.0.0.1',
    '--port', '27017',
    '--logpath', "`"$dados\mongod.log`"",
    '--logappend'
)

Start-Sleep -Seconds 4

if (Get-Process mongod -ErrorAction SilentlyContinue) {
    Write-Host 'MongoDB iniciado em 127.0.0.1:27017'
    Write-Host 'Para encerrar: scripts\parar_mongodb.bat'
} else {
    Write-Host "ERRO ao iniciar o MongoDB. Veja o log:`n  $dados\mongod.log"
    exit 1
}
