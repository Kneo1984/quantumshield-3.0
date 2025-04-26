# lex_supervisor_socketlink.py
# 🌐 Sende Befehle von Windows (LEX) zu ShadowCore (Linux)
# Kategorisiert, nummerisch wählbar, sprachlich rückgemeldet

import socket       # Netzwerkverbindung
import pyttsx3      # TTS für Antwort
import time         # Pausen

# 🧠 Sprachausgabe initialisieren
engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("voice", engine.getProperty("voices")[0].id)

def sprich(text):
    print(f"LEX sagt: {text}")
    engine.say(text)
    engine.runAndWait()

# 🔌 Verbindung zu ShadowCore
def sende_befehl(befehl):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("172.26.162.25", 19840))  # Deine Kali-IP prüfen!
            s.sendall(befehl.encode("utf-8"))
            sprich(f"Befehl gesendet an ShadowCore: {befehl}")
    except Exception as e:
        sprich(f"Verbindung fehlgeschlagen: {e}")

# 📋 Menüsystem mit Nummernsteuerung
def supervisor_menu():
    while True:
        print("\n🧠 QuantumShield → ShadowCore Menü")
        print("1️⃣ → apt update")
        print("2️⃣ → Öffne Firefox")
        print("3️⃣ → Öffne Dateibrowser (xdg-open .)")
        print("4️⃣ → Starte htop")
        print("5️⃣ → Exit")

        wahl = input("Nummer eingeben (1–5): ").strip()

        if wahl == "1":
            sende_befehl("apt update")
        elif wahl == "2":
            sende_befehl("firefox")
        elif wahl == "3":
            sende_befehl("xdg-open .")
        elif wahl == "4":
            sende_befehl("htop")
        elif wahl == "5":
            sprich("Supervisor beendet Verbindung. Bis bald.")
            break
        else:
            sprich("Ungültige Eingabe. Bitte erneut versuchen.")

# 🔁 Autostart
if __name__ == "__main__":
    supervisor_menu()

# 🌌 QuantumShield → ShadowCore Menü
def quantumshield_shadowcore_menue():
    print("\n🛡️ QuantumShield → ShadowCore Menü")
    print("1) apt update")
    print("2) apt upgrade")
    print("3) Öffne Dateimanager (xdg-open .)")
    print("4) Öffne Microsoft Edge")
    print("5) htop (wenn installiert)")
    print("6) Zurück")

    auswahl = input("Wähle (1–6): ").strip()

    befehle = {
        "1": "apt update",
        "2": "apt upgrade",
        "3": "xdg-open .",
        "4": "microsoft-edge",
        "5": "htop"
    }

    if auswahl in befehle:
        sende_befehl(befehle[auswahl])
    elif auswahl == "6":
        return
    else:
        print("Ungültige Eingabe.")
