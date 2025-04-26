import pyttsx3
import speech_recognition as sr
import os
import subprocess
import time

# Initialisiere TTS
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Männlich (anpassbar)

# Sprechfunktion mit Sicherheit
def sprich(text):
    print(f"LEX sagt: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Fehler beim Sprechen: {e}")

# Spracheingabe
def erkenne_befehl():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        sprich("LEX hört...")
        try:
            audio = recognizer.listen(source, timeout=5)
            befehl = recognizer.recognize_google(audio, language="de-DE")
            print(f"Erkannt: {befehl}")
            return befehl.lower()
        except sr.UnknownValueError:
            sprich("Ich habe dich nicht verstanden. Wiederhole bitte, KNEO.")
        except sr.WaitTimeoutError:
            sprich("Niemand spricht. Ich warte erneut.")
        except Exception as e:
            sprich("Fehler bei der Spracheingabe.")
            print(e)
    return None

# SUPERVISOR MODUS
def supervisor_modus():
    sprich("Supervisor-Modus aktiviert. Ich übernehme nun deine Aufgaben.")
    while True:
        befehl = erkenne_befehl()
        if befehl:
            # Explorer öffnen
            if "explorer" in befehl or "dokumente" in befehl:
                sprich("Ich öffne den Explorer für dich.")
                os.startfile("C:\\Users\\denni\\Documents")
            # YouTube öffnen
            elif "youtube" in befehl or "browser" in befehl:
                sprich("Ich öffne YouTube im Browser.")
                subprocess.Popen(["start", "https://youtube.com"], shell=True)
            # Erinnerung
            elif "erinnerung" in befehl:
                with open("lex_erinnerung.txt", "a", encoding="utf-8") as f:
                    f.write(f"{time.ctime()}: {befehl}\n")
                sprich("Ich habe es mir gemerkt.")
            # Beenden
            elif "beenden" in befehl or "ruhe" in befehl:
                sprich("LEX geht jetzt offline. Bis bald, KNEO.")
                break
            # Unbekannter Befehl
            else:
                sprich(f"Ich habe verstanden: {befehl}. Aber keine Aktion ist damit verknüpft.")

        time.sleep(0.5)

# Hauptstart
if __name__ == "__main__":
    sprich("LEX meldet sich. Sag 'Supervisor-Modus aktivieren', um zu starten.")
    while True:
        befehl = erkenne_befehl()
        if befehl and "supervisor" in befehl:
            supervisor_modus()
            break
