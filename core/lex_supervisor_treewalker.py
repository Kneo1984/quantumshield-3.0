import pyttsx3
import speech_recognition as sr
import os
import subprocess
from pathlib import Path
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def sprich(text):
    print(f"LEX sagt: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Sprachfehler: {e}")

def erkenne_befehl():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=6)
            befehl = recognizer.recognize_google(audio, language="de-DE")
            print(f"Erkannt: {befehl}")
            return befehl.lower()
        except:
            return None

def finde_datei(basis, name):
    for pfad in Path(basis).rglob("*"):
        if name.lower() in pfad.name.lower():
            return str(pfad)
    return None

def supervisor_modus():
    sprich("Supervisor-Modus vollständig aktiv.")
    while True:
        befehl = erkenne_befehl()
        if not befehl:
            continue

        if "explorer" in befehl or "desktop" in befehl:
            os.startfile(os.path.expanduser("~/Desktop"))
            sprich("Desktop geöffnet.")

        elif "shadowcore" in befehl:
            shadowpath = os.path.expanduser("~/Desktop/ShadowCore")
            if os.path.exists(shadowpath):
                os.startfile(shadowpath)
                sprich("Ordner ShadowCore geöffnet.")
            else:
                sprich("Ordner ShadowCore existiert nicht.")

        elif "starte" in befehl:
            if "edge" in befehl:
                subprocess.Popen("start msedge", shell=True)
                sprich("Edge wird gestartet.")
            elif "word" in befehl:
                subprocess.Popen("start winword", shell=True)
                sprich("Word wird gestartet.")
            elif "vs code" in befehl or "visual studio" in befehl:
                subprocess.Popen("code", shell=True)
                sprich("VS Code wird gestartet.")
            else:
                sprich("Starte-Befehl erkannt, aber kein bekanntes Ziel.")

        elif "finde" in befehl or "suche" in befehl:
            wort = befehl.split()[-1]
            datei = finde_datei("C:\\Users\\denni", wort)
            if datei:
                os.startfile(datei)
                sprich(f"Datei {wort} gefunden und geöffnet.")
            else:
                sprich(f"Ich konnte {wort} nicht finden.")

        elif "öffne datei" in befehl:
            name = befehl.replace("öffne datei", "").strip()
            pfad = finde_datei("C:\\Users\\denni", name)
            if pfad:
                os.startfile(pfad)
                sprich(f"Datei {name} geöffnet.")
            else:
                sprich(f"Datei {name} nicht gefunden.")

        elif "beenden" in befehl:
            sprich("LEX Supervisor-Modus wird jetzt deaktiviert.")
            break

        else:
            sprich(f"Befehl erkannt: {befehl}. Noch keine definierte Aktion.")
        time.sleep(0.5)

if __name__ == "__main__":
    sprich("LEX aktiviert. Supervisor-Modus bereit.")
    while True:
        befehl = erkenne_befehl()
        if befehl and "supervisor" in befehl:
            supervisor_modus()
            break
