import pyttsx3                      # TTS-Modul
import speech_recognition as sr     # Spracheingabe
import os                           # Systembefehle
import time                         # Begrüßungsverzögerung

# Stimme definieren
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # männliche Stimme auswählen

# Begrüßung sprechen
def begruessung():
    engine.say("Willkommen zurück, KNEO. Ich bin LEX. Bereit zur Steuerung.")
    engine.runAndWait()

# Spracheingabe starten
def erkenne_befehl():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("LEX hört zu...")
        audio = recognizer.listen(source)

    try:
        befehl = recognizer.recognize_google(audio, language='de-DE')
        print(f"Kommando erkannt: {befehl}")
        return befehl.lower()
    except sr.UnknownValueError:
        print("LEX konnte dich nicht verstehen.")
        return None

# Hauptfunktion
def lex_start():
    begruessung()
    while True:
        befehl = erkenne_befehl()
        if befehl and "ordner erstellen" in befehl:
            pfad = "C:\\Users\\denni\\Desktop\\NeuerOrdner"
            os.makedirs(pfad, exist_ok=True)
            engine.say("Ordner wurde erstellt.")
            engine.runAndWait()
        elif befehl and "beenden" in befehl:
            engine.say("LEX beendet. Bis bald, KNEO.")
            engine.runAndWait()
            break

if __name__ == "__main__":
    lex_start()
