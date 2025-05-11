Write-Host ""
Write-Host " 🚀 Starte QuantumShield™ 3.0 Installation + Start..." -ForegroundColor Cyan
Write-Host ""

# Installations-Skript starten
if (Test-Path ".\install_quantumshield.ps1") {
    Write-Host " 🛠️  Führe Installations-Skript aus..." -ForegroundColor Green
    .\install_quantumshield.ps1
} else {
    Write-Host " ❌ Installations-Skript nicht gefunden!" -ForegroundColor Red
    exit
}

# Hauptsystem starten
if (Test-Path ".\start_quantumshield.bat") {
    Write-Host ""
    Write-Host " ✅ QuantumShield wird gestartet..." -ForegroundColor Green
    Start-Process .\start_quantumshield.bat
} else {
    Write-Host " ❌ Startdatei nicht gefunden!" -ForegroundColor Red
}

