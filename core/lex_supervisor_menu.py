# lex_supervisor_menu.py
# 🌌 LEX SUPERVISOR-MODUS – QuantumShield Kontrolleinheit
# 🧠 Steuerung über Zahlen-Eingabe mit Sprachfeedback
# 💬 Spracheingabe bewusst deaktiviert – nur Rückmeldung per Stimme

import pyttsx3                          # Für Sprachausgabe
import time                             # Für weiche Übergänge
import lex_dateisuche                   # 📂 Modul: Dateisuche
import lex_sprachlog                    # 📋 Modul: Sprachlog
import lex_sicherheitslayer             # 🛡️ Modul: Sicherheitsprüfung
import lex_lernsystem                   # 🧠 Modul: Lernsystem
import lex_supervisor_socketlink        # 📡 Verbindung zu ShadowCore

# 🎙️ TTS Engine starten
engine = pyttsx3.init()
engine.setProperty("rate", 180)  # Sprachgeschwindigkeit
engine.setProperty("voice", engine.getProperty("voices")[0].id)

# 🔊 Sprachfeedback
def sprich(text):
    print(f"LEX sagt: {text}")
    engine.say(text)
    engine.runAndWait()

# 📋 Menü anzeigen
def zeige_menue():
    print("\n🔹 SUPERVISOR MODUS – Steuerung:")
    print("1️⃣ Dateisuche starten")
    print("2️⃣ Sprachlog anzeigen")
    print("3️⃣ Sicherheitsprüfung aktivieren")
    print("4️⃣ Lernsystem starten")
    print("5️⃣ Exit sauber")
    print("6️⃣ ShadowCore Menü (Netzwerkbefehl)\n")

# 🧠 Menü-Logik
def supervisor_menu():
    sprich("Willkommen im LEX Supervisor-Modus, KNEO.")
    time.sleep(1)

    while True:
        zeige_menue()
        eingabe = input("🔢 Gib eine Nummer (1–6) ein: ").strip()

        if eingabe == "1":
            sprich("Starte Dateisuche.")
            lex_dateisuche.starte_dateisuche()

        elif eingabe == "2":
            sprich("Zeige gespeicherten Sprachlog.")
            lex_sprachlog.letzter_befehl()

        elif eingabe == "3":
            sprich("Starte Sicherheitsüberprüfung.")
            befehl = input("🔐 Gib den Befehl ein, den du prüfen willst: ")
            if lex_sicherheitslayer.pruefe_befehl(befehl):
                sprich(f"Befehl {befehl} ist sicher.")
            else:
                sprich(f"Befehl {befehl} wurde blockiert.")

        elif eingabe == "4":
            sprich("Analysiere meistgenutzte Befehle.")
            lex_lernsystem.zeige_haeufigste_befehle()

        elif eingabe == "5":
            sprich("Supervisor-Modus beendet. Bis bald, KNEO.")
            break

        elif eingabe == "6":
            sprich("QuantumShield ShadowCore Menü wird geöffnet.")
            lex_supervisor_socketlink.quantumshield_shadowcore_menue()

        else:
            sprich("Ungültige Eingabe. Bitte versuche es erneut.")

# 🟢 Startpunkt
if __name__ == "__main__":
    supervisor_menu()
