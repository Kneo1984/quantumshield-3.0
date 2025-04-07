import socket
import datetime
import time

# Lokale IP-Adresse
ip = socket.gethostbyname(socket.gethostname())

# Zeitstempel
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Log-Eintrag
with open("shield.log", "a") as log:
    log.write(f"[{timestamp}] QuantumShield aktiviert | IP: {ip}\n")

# Terminalausgabe (wenn du die Konsole sehen willst)
print("QuantumShield wurde aktiviert.")
print(f"IP: {ip}")
print("Log wurde gespeichert.")

# Halte den Prozess 60 Sekunden im RAM
time.sleep(60)
