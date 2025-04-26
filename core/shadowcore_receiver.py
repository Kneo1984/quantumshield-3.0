# shadowcore_receiver.py
# 🛡️ ShadowCore – Empfangsmodul für LEX
# Wartet auf Befehle über Socket und führt sie sicher aus – mit Logging
import shadowcore_logger
import socket             # Netzwerk
import subprocess         # Ausführung
import os                 # Systemzugriff
from datetime import datetime  # Zeitstempel für Logging

# 📜 Logging-Modul integriert
def logge_befehl(befehl):
    zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logzeile = f"[{zeit}] {befehl}\n"
    with open("/root/shadowcore_befehle.log", "a", encoding="utf-8") as logfile:
        logfile.write(logzeile)
# shadowcore_logger.py
from datetime import datetime

def logge_befehl(befehl):
    zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logzeile = f"[{zeit}] {befehl}\n"
    with open("/root/shadowcore_befehle.log", "a", encoding="utf-8") as logfile:
        logfile.write(logzeile)

# 🌐 Socket-Konfiguration
HOST = "0.0.0.0"
PORT = 19840

# 🔊 Starte Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[🛡️] ShadowCore aktiv und wartend auf LEX...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"\n[↘️] Befehl von {addr}:")
            data = conn.recv(2048).decode("utf-8").strip()

            if not data:
                print("⚠️ Kein Befehl empfangen.")
                continue

            # 🧠 Logge Befehl
            logge_befehl(data)

            print(f"[⚙️] Ausführung: {data}")
            try:
                result = subprocess.run(data, shell=True, capture_output=True, text=True, executable="/bin/bash")

                if result.stdout:
                    print(f"[✅] Ausgabe:\n{result.stdout}")
                if result.stderr:
                    print(f"[❌] Fehler:\n{result.stderr}")
            except Exception as e:
                print(f"[🚨] Ausnahme bei Ausführung: {e}")
