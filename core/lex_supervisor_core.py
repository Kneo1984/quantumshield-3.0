# lex_supervisor_core.py
# 🌌 LEX Supervisor-Modus – QuantumShield KI-Terminal
# 💡 Funktionen: Sprachsteuerung, Nummerneingabe, Root-Kommandos, Kategorien

import speech_recognition as sr        # Spracheingabe
import pyttsx3                         # Sprachausgabe
import socket                          # Netzwerkverbindung (Socket)
import os                              # Systemfunktionen
import subprocess                      # Root-Kommandos
import time                            # Zeitverzögerung

# 🧠 Sprachausgabe initialisieren
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)

# 🔗 Kategorien & Befehle: Nummer → (Kategorie, Shell-Befehl)
befehle = {
    1: ("System", "apt update"),
    2: ("System", "apt upgrade"),
    3: ("Web", "firefox https://youtube.com"),
    4: ("Dateien", "thunar"),
    5: ("Dateien", "xdg-open ~/Dokumente"),
    6: ("Protokoll", "xdg-open Projektstatus_LEX_ShadowCore.md"),
    7: ("Root", "gnome-terminal -- bash -c 'sudo su'"),
    8: ("Mission", "echo 'Unsere Mission: Schutz, Bewusstsein, Verbindung.'"),
    9: ("Suche", "find ~ -name '*.pdf'"),
}

# 🔊 Sprachfeedback
def sprich(text):
    print(f"LEX sagt: {text}")
    engine.say(text)
    engine.runAndWait()

# 🎙️ Sprache erkennen
def erkenne_befehl():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        sprich("Ich höre zu, KNEO.")
        audio = r.listen(source)
    try:
        befehl = r.recognize_google(audio, language="de-DE")
        print(f"🔎 Erkannt: {befehl}")
        return befehl.lower()
    except sr.UnknownValueError:
        sprich("Ich habe dich nicht verstanden.")
        return None

# 📡 Befehl senden an ShadowCore
def sende_befehl(befehl):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 19840))
            s.sendall(befehl.encode("utf-8"))
            sprich(f"Befehl gesendet: {befehl}")
    except:
        sprich("Verbindung zu ShadowCore fehlgeschlagen.")

# 🔢 Nummernbefehl lokal per Eingabe starten
def nummer_eingabe():
    print("\n🔢 Verfügbare Befehle:")
    for nummer, (kategorie, befehl) in befehle.items():
        print(f"{nummer}) [{kategorie}] → {befehl}")
    auswahl = input("Gib eine Nummer ein: ")
    if auswahl.isdigit():
        auswahl = int(auswahl)
        if auswahl in befehle:
            sende_befehl(befehle[auswahl][1])
        else:
            print("Ungültige Nummer.")
    else:
        print("Nur Zahlen erlaubt.")

# 🚀 Hauptfunktion – Sprach- oder Tastenmodus
def supervisor_start():
    sprich("LEX Supervisor-Modus aktiviert. Sag etwas oder gib eine Zahl ein.")
    while True:
        modus = input("\nWähle 'sprache', 'nummer' oder 'exit': ").strip().lower()
        if modus == "sprache":
            befehl = erkenne_befehl()
            if befehl:
                for nummer, (kategorie, cmd) in befehle.items():
                    if any(wort in befehl for wort in cmd.split()):
                        sende_befehl(cmd)
                        break
        elif modus == "nummer":
            nummer_eingabe()
        elif modus == "exit":
            sprich("LEX beendet den Supervisor-Modus. Bis bald.")
            break
        else:
            print("Ungültige Eingabe.")

# 🧠 Starte Supervisor-Modus
if __name__ == "__main__":
    supervisor_start()
