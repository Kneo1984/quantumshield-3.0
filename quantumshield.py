# quantumshield_diagnose.py – Vollständige Systemdiagnose mit UTF-8 Support

import socket
import datetime
import os
import platform
import psutil  # 🔍 Für CPU, RAM, etc.

# 📁 Dateipfade
logfile_main = "shield.log"
logfile_diag = "shield_diagnose.log"

# 🔧 Stelle sicher, dass alles als UTF-8 geschrieben wird
def write_log(file, content):
    with open(file, "a", encoding="utf-8") as f:
        f.write(content + "\n")

# 🌐 IP-Adresse ermitteln
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# 🕒 Zeitstempel erstellen
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 💻 Systeminfos erfassen
system_name = platform.system()
system_version = platform.version()
architecture = platform.machine()
processor = platform.processor()
cpu_cores = psutil.cpu_count(logical=False)
cpu_threads = psutil.cpu_count(logical=True)
ram_total = round(psutil.virtual_memory().total / (1024**3), 2)

# 📦 Speicherplatz
disk = psutil.disk_usage('/')
disk_total = round(disk.total / (1024**3), 2)
disk_used = round(disk.used / (1024**3), 2)

# 🛡️ Hauptlog schreiben
write_log(logfile_main, f"[{timestamp}] 🛡️ QuantumShield aktiviert auf {local_ip}")

# 🧪 Diagnoselog schreiben
write_log(logfile_diag, "==================== QuantumShield Systemdiagnose ====================")
write_log(logfile_diag, f"[🔐] QuantumShield gestartet – {timestamp}")
write_log(logfile_diag, f"[📁] Arbeitsverzeichnis: {os.getcwd()}")
write_log(logfile_diag, f"[🖥️] Hostname: {hostname}")
write_log(logfile_diag, f"[🌐] IP-Adresse: {local_ip}")
write_log(logfile_diag, f"[💾] Speicherplatz: {disk_used} GB von {disk_total} GB belegt")
write_log(logfile_diag, f"[🧠] RAM: {ram_total} GB")
write_log(logfile_diag, f"[⚙️] CPU: {processor} ({cpu_cores} Kerne / {cpu_threads} Threads)")
write_log(logfile_diag, f"[🖥️] OS: {system_name} {system_version} ({architecture})")
write_log(logfile_diag, f"[✅] Status: Diagnose abgeschlossen")

# 📢 Direkte Ausgabe im Terminal (optional)
print("✅ QuantumShield aktiviert")
print(f"🔍 IP-Adresse:        {local_ip}")
print(f"🧠 RAM:              {ram_total} GB")
print(f"⚙️ CPU:              {processor} ({cpu_cores} Kerne, {cpu_threads} Threads)")
print(f"💾 Speicher:         {disk_used}/{disk_total} GB belegt")
print(f"📁 Arbeitsverzeichnis: {os.getcwd()}")
print(f"🕒 Zeitstempel:       {timestamp}")
print("📜 Logs geschrieben in:")
print(f"   → {logfile_main}")
print(f"   → {logfile_diag}")

