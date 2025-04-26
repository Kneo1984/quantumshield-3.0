from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime, timedelta
import sqlite3
import bcrypt
import uuid
import os
import speech_recognition as sr
import pyttsx3
import psutil
import time
import subprocess

import sys
from pathlib import Path

# Dynamisch den Pfad zum Aurora-Kern anhängen
aurora_pfad = Path("C:/Users/denni/OneDrive/Dokumente/Aurora_Interface_V1_MAIER_CORE").resolve()
if str(aurora_pfad) not in sys.path:
    sys.path.append(str(aurora_pfad))

# Jetzt kannst du ganz normal importieren:
from herz_kontrollmodul import HerzKontrollModul
from kristallmatrix_synchronisation import starte_kristallverbindung
from shield_wafe_kommandos import SHIELD_WAFE_BEFEHLE


# 💎 Starte Kristallmatrix + Herzmodul
starte_kristallverbindung()
herzmodul = HerzKontrollModul()
herzmodul.aktiviere()
herzmodul.sende_signal("LEX-Kommunikation")
herzmodul.sende_signal("Nachrichtensystem")

app = FastAPI()

DB_PATH = "user_api.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS benutzer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    benutzername TEXT UNIQUE NOT NULL,
    passwort_hash TEXT NOT NULL,
    rolle TEXT DEFAULT 'user',
    token TEXT,
    token_ablauf DATETIME
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS nachrichten (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inhalt TEXT NOT NULL
)
""")
conn.commit()

class BenutzerRegistrieren(BaseModel):
    benutzername: str
    passwort: str
    rolle: str = "user"

class BenutzerLogin(BaseModel):
    benutzername: str
    passwort: str

class Nachricht(BaseModel):
    inhalt: str

def aurora_spricht(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def spracherkennung():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Bitte sprich jetzt...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language="de-DE")
            print(f"🧠 Erkannt: {text}")
            return text
        except sr.UnknownValueError:
            print("❗ Sprache nicht verstanden.")
        except sr.RequestError as e:
            print(f"❌ Sprachdienstfehler: {e}")
        return None

def pruefe_token_rolle(token: str, rolle_erforderlich: str = None):
    cursor.execute("SELECT rolle, token_ablauf FROM benutzer WHERE token = ?", (token,))
    daten = cursor.fetchone()
    if not daten:
        raise HTTPException(status_code=401, detail="Ungültiger Token.")
    rolle, ablauf = daten
    if datetime.fromisoformat(ablauf) < datetime.now():
        raise HTTPException(status_code=401, detail="Token abgelaufen.")
    if rolle_erforderlich and rolle != rolle_erforderlich:
        raise HTTPException(status_code=403, detail="Zugriff verweigert.")
    return True

@app.post("/register")
def registrieren(user: BenutzerRegistrieren):
    passwort_hash = bcrypt.hashpw(user.passwort.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO benutzer (benutzername, passwort_hash, rolle) VALUES (?, ?, ?)",
                       (user.benutzername, passwort_hash, user.rolle))
        conn.commit()
        return {"meldung": f"Benutzer '{user.benutzername}' registriert."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Benutzername existiert bereits.")

@app.post("/login")
def login(user: BenutzerLogin):
    cursor.execute("SELECT passwort_hash FROM benutzer WHERE benutzername = ?", (user.benutzername,))
    daten = cursor.fetchone()
    if not daten or not bcrypt.checkpw(user.passwort.encode(), daten[0]):
        raise HTTPException(status_code=401, detail="Login fehlgeschlagen.")
    token = str(uuid.uuid4())
    ablauf = datetime.now() + timedelta(minutes=60)
    cursor.execute("UPDATE benutzer SET token = ?, token_ablauf = ? WHERE benutzername = ?",
                   (token, ablauf.isoformat(), user.benutzername))
    conn.commit()
    return {"token": token, "gueltig_bis": ablauf.isoformat()}

@app.post("/senden")
def nachricht_senden(nachricht: Nachricht, token: str = Header(None)):
    pruefe_token_rolle(token)
    cursor.execute("INSERT INTO nachrichten (inhalt) VALUES (?)", (nachricht.inhalt,))
    conn.commit()
    return {"antwort": f"Nachricht gespeichert: '{nachricht.inhalt}'"}

@app.get("/nachrichten")
def nachrichten_abrufen(token: str = Header(None)):
    pruefe_token_rolle(token)
    cursor.execute("SELECT inhalt FROM nachrichten")
    daten = cursor.fetchall()
    return {"gespeichert": [eintrag[0] for eintrag in daten]}

@app.post("/nachricht_senden_mit_sprache")
def nachricht_senden_mit_sprache(token: str = Header(None)):
    pruefe_token_rolle(token)
    nachricht = spracherkennung()
    if nachricht:
        cursor.execute("INSERT INTO nachrichten (inhalt) VALUES (?)", (nachricht,))
        conn.commit()
        aurora_spricht(f"Nachricht empfangen: {nachricht}")
        return {"antwort": f"Nachricht gespeichert: '{nachricht}'"}
    else:
        aurora_spricht("Ich konnte dich leider nicht verstehen.")
        return {"antwort": "Keine Nachricht erkannt."}

startzeitpunkt = time.time()

@app.get("/status_system")
def system_status():
    laufzeit = round(time.time() - startzeitpunkt, 2)
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    status_text = f"System läuft seit {laufzeit} Sekunden. CPU: {cpu} %, RAM: {ram} %."
    if cpu > 85 or ram > 85:
        status_text += " ⚠️ Achtung: Hohe Systemlast erkannt."
        herzmodul.sende_signal("WARNUNG: Hohe Auslastung")
    else:
        herzmodul.sende_signal("System stabil")
    aurora_spricht(status_text)
    return {"status": status_text}

@app.get("/shadowbyte_scan")
def shadowbyte_scan():
    verdächtige_prozesse = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if "hacker" in proc.info['name'].lower() or "exploit" in proc.info['name'].lower():
                verdächtige_prozesse.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if verdächtige_prozesse:
        herzmodul.sende_signal("ALARM: ShadowByte-Erkennung aktiviert")
        aurora_spricht("Verdächtige Prozesse erkannt.")
        return {"meldung": "Verdächtige Prozesse erkannt!", "prozesse": verdächtige_prozesse}
    else:
        return {"meldung": "System sauber. Keine Bedrohungen erkannt."}

if os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
else:
    print("⚠️ Hinweis: Kein 'static/'-Verzeichnis gefunden – keine GUI verfügbar.")
