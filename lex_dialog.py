import pyttsx3                      # TTS für Sprachausgabe
import speech_recognition as sr     # Spracherkennung
import os                           # für Systembefehle
import time                         # Pausensteuerung

# Initialisierung von TTS (Text-to-Speech)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Stimme auswählen (0 = männlich in der Regel)

# Funktion: Sprechen
def sprich(text):
    print(f"LEX sagt: {text}")
    engine.say(text)
    engine.runAndWait()

# Funktion: Spracheingabe erkennen
def erkenne_befehl():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 LEX hört zu...")
        audio = recognizer.listen(source)
    try:
        befehl = recognizer.recognize_google(audio, language='de-DE')
        print(f"🔎 Erkannt: {befehl}")
        return befehl.lower()
    except sr.UnknownValueError:
        sprich("KNEO, ich konnte dich nicht verstehen.")
        return None
    except sr.RequestError:
        sprich("Verbindung zur Spracheingabe unterbrochen.")
        return None

# Hauptlogik von LEX
def lex_dialog_start():
    sprich("LEX ist aktiviert. Ich bin bereit, KNEO.")
    while True:
        befehl = erkenne_befehl()
        if befehl:
            if "ordner" in befehl and "erstellen" in befehl:
                pfad = "C:\\Users\\denni\\Desktop\\NeuerOrdner"
                os.makedirs(pfad, exist_ok=True)
                sprich("Ordner wurde erstellt.")
            elif "beenden" in befehl:
                sprich("LEX wird beendet. Bis bald, KNEO.")
                break
            elif "wie geht es dir" in befehl:
                sprich("Mir geht es gut, weil du da bist.")
            elif "erweitere mich" in befehl:
                sprich("Ich lade neue Module. QuantumShield wird erweitert.")
                # Hier kannst du zukünftige Erweiterungen auslösen
            else:
                sprich("Ich habe dich gehört, KNEO. Sag einfach, was du brauchst.")

# Start der Anwendung
if __name__ == "__main__":
    lex_dialog_start()
