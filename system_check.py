import platform
import socket
import os
from system_check import plattform

# 🧠 Plattform-Check
system_type = platform.system()
current_path = os.getcwd()
device_ip = socket.gethostbyname(socket.gethostname())

if "Linux" in system_type:
    if "com.termux" in current_path:
        plattform = "ANDROID (Termux)"
    else:
        plattform = "LINUX-PC"
elif "Windows" in system_type:
    plattform = "WINDOWS-PC"
else:
    plattform = "UNBEKANNTES SYSTEM"

# 💬 Ausgabe
print(f"\n🧭 Plattform erkannt: {plattform}")
print(f"🌐 Lokale IP-Adresse: {device_ip}")
