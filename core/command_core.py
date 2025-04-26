import platform
import socket

# === SYSTEM-ERKENNUNG ===
system_type = platform.system()
device_ip = socket.gethostbyname(socket.gethostname())

if "Linux" in system_type:
    if "com.termux" in os.getcwd():
        plattform = "ANDROID (Termux)"
    else:
        plattform = "LINUX PC"
elif "Windows" in system_type:
    plattform = "WINDOWS PC"
else:
    plattform = "UNBEKANNTES SYSTEM"

# === AUSGABE & LOGGING ===
print(f"\n🧭 Plattform erkannt: {plattform}")
print(f"🌐 Lokale IP: {device_ip}")
