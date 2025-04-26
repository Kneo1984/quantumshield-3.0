# quantumshield.py – Sichtbarer Schutzmodus für Prozessprüfung

import socket       # Für die lokale IP-Adresse
import datetime     # Für den Zeitstempel
import time         # Für künstliche Laufzeit

# 🛰️ Lokale IP ermitteln
ip = socket.gethostbyname(socket.gethostname())

# 🕒 Zeitstempel generieren
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 📝 Log-Eintrag speichern
with open("shield.log", "a") as log:
    log.write(f"[{timestamp}] QuantumShield aktiviert | IP: {ip}\n")

# 💬 Sichtbare Ausgabe im Terminal
print("🛡️ QuantumShield wurde aktiviert.")
print(f"📍 Lokale IP: {ip}")
print("📄 Log wurde erfolgreich geschrieben.")

# ⏳ Halte den Prozess 60 Sekunden im Speicher
time.sleep(60)
