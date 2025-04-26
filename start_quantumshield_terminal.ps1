from pathlib import Path

# PowerShell-Skript zur automatisierten Ausführung vorbereiten
powershell_script = r'''
Start-Process powershell -ArgumentList "uvicorn main_shadowbyte:app --reload" -NoNewWindow
Start-Sleep -Seconds 5
Start-Process python -ArgumentList "quantumshield_gui_terminal.py"
'''

# Speicherort im Projektverzeichnis
ps1_path = Path("/mnt/data/start_quantumshield_terminal.ps1")
ps1_path.write_text(powershell_script, encoding="utf-8")

ps1_path.name
