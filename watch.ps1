# watch.ps1
param(
    [string]$ProjectRoot = (Get-Location).Path
)

Write-Host "👀 Observando alterações em $ProjectRoot…" -ForegroundColor Cyan

# Configura o FileSystemWatcher
$fsw = New-Object System.IO.FileSystemWatcher $ProjectRoot, '*.py' `
    -Property @{
        IncludeSubdirectories = $true
        NotifyFilter = [System.IO.NotifyFilters]'LastWrite'
    }

# Ação a executar quando um .py mudar
$action = {
    # Pequena pausa para o editor terminar de gravar o arquivo
    Start-Sleep -Milliseconds 200

    Write-Host "⚙️  Mudança detectada em $($Event.SourceEventArgs.FullPath). Reconstruindo .exe…" -ForegroundColor Yellow

    # Ativa o venv
    & .\venv\Scripts\Activate

    # Roda o PyInstaller (ajuste flags conforme seu setup)
    pyinstaller --onedir --windowed `
      --add-data "database\db.sqlite3;database" `
      --add-data "ui;ui" `
      --clean `
      main.py

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Build concluído com sucesso em $(Get-Date -Format T)" -ForegroundColor Green
    } else {
        Write-Host "❌ Erro no build (exit code $LASTEXITCODE)." -ForegroundColor Red
    }
}

# Registra eventos
Register-ObjectEvent $fsw Changed  -Action $action | Out-Null
Register-ObjectEvent $fsw Created  -Action $action | Out-Null
Register-ObjectEvent $fsw Deleted  -Action $action | Out-Null
Register-ObjectEvent $fsw Renamed  -Action $action | Out-Null

# Mantém o watcher vivo
while ($true) { Start-Sleep -Seconds 1 }
