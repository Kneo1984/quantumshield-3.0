# quantumshield.py – QuantumShield™ 3.0 Prototyp

#  Module für Netzwerk, Zeit, Systeminfos
import socket
import datetime
import os

#  Diagnose-Log vorbereiten
diagnose_logfile = "shield_diagnose.log"
with open(diagnose_logfile, "a") as diag_log:
    diag_log.write("\n====================\n")
    diag_log.write(f"[🔐] QuantumShield gestartet – {datetime.datetime.now()}\n")
    diag_log.write(f"[📁] Ausgeführt von: {os.getcwd()}\n")

# 📡 Schritt 1: Lokale IP-Adresse ermitteln
ip = socket.gethostbyname(socket.gethostname())

# 🕒 Schritt 2: Zeitstempel erzeugen
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 📜 Schritt 3: Standard-Log aktualisieren
with open("shield.log", "a") as log:
    log.write(f"[{timestamp}] QuantumShield aktiviert auf IP {ip}\n")

# 🔁 Diagnose-Log erweitern
with open(diagnose_logfile, "a") as diag_log:
    diag_log.write(f"[📡] Lokale IP-Adresse: {ip}\n")
    diag_log.write(f"[🕒] Zeitstempel: {timestamp}\n")
    diag_log.write(f"[✅] Status: Aktivierung erfolgreich\n")
