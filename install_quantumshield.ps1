# QuantumShield 3.0 Installations-Skript
Write-Host ' QuantumShield 3.0 Installation gestartet...'

# Installiere benötigte Python-Packages
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host " requirements.txt nicht gefunden!"
}

# Setze Startrechte für .sh Skripte (nur Linux)
if (Test-Path "start_quantumshield.sh") {
    chmod +x start_quantumshield.sh
}

# Teste ob Startdateien existieren
if (Test-Path "start_quantumshield.bat") {
    Write-Host ' Startdatei start_quantumshield.bat gefunden.'
} else {
    Write-Host ' Startdatei start_quantumshield.bat fehlt!'
}

if (Test-Path "core\quantumshield.py") {
    Write-Host ' Hauptmodul core\quantumshield.py vorhanden.'
} else {
    Write-Host ' Hauptmodul core\quantumshield.py fehlt!'
}

# Erfolgsnachricht
Write-Host ' QuantumShield 3.0 Installation abgeschlossen!'
Write-Host ' Starte das System mit: .\start_quantumshield.bat'
