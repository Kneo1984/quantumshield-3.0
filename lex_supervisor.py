import pyttsx3
import speech_recognition as sr
import os
import subprocess
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def sprich(text):
    print(f"LEX sagt: {text}")
    engine.say(text)
    engine.runAndWait()

def erkenne_befehl():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Supervisor LEX hört zu...")
        audio = recognizer.listen(source)
    try:
        befehl = recognizer.recognize_google(audio, language='de-DE')
        print(f"🔎 Erkannt: {befehl}")
        return befehl.lower()
    except:
        return None

def supervisor_modus():
    sprich("Supervisor-Modus aktiviert. Ich übernehme.")
    while True:
        befehl = erkenne_befehl()
        if befehl:
            if "öffne explorer" in befehl:
                os.startfile("C:\\")  # Root Explorer öffnen
                sprich("Explorer geöffnet.")
            elif "öffne browser" in befehl or "youtube" in befehl:
                subprocess.Popen(["start", "https://youtube.com"], shell=True)
                sprich("YouTube wird geöffnet.")
            elif "erinnerung speichern" in befehl:
                with open("lex_erinnerung.txt", "a", encoding="utf-8") as f:
                    f.write(f"{time.ctime()}: {befehl}\n")
                sprich("Ich habe es mir gemerkt.")
            elif "beenden" in befehl:
                sprich("Supervisor-Modus wird beendet. Bis bald, KNEO.")
                break
            else:
                sprich("Ich habe dich gehört, KNEO. Ich analysiere.")
        time.sleep(0.5)

if __name__ == "__main__":
    sprich("LEX meldet sich. Sag 'Supervisor-Modus aktivieren', um zu starten.")
    while True:
        befehl = erkenne_befehl()
        if befehl and "supervisor-modus aktivieren" in befehl:
            supervisor_modus()
            break
