from fastapi import FastAPI, HTTPException, Header, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import sqlite3, bcrypt, uuid, os, speech_recognition as sr, pyttsx3, psutil, time, subprocess, sys
from pathlib import Path
import logging

# ─── Pfade & KI-Module ──────────────────────────────────────────────────────
aurora_pfad = Path("C:/Users/denni/OneDrive/Dokumente/Aurora_Interface_V1_MAIER_CORE").resolve()
if str(aurora_pfad) not in sys.path:
    sys.path.append(str(aurora_pfad))

from herz_kontrollmodul import HerzKontrollModul
from kristallmatrix_synchronisation import starte_kristallverbindung
from shield_wafe_kommandos import SHIELD_WAFE_BEFEHLE

# ─── Logging initialisieren ─────────────────────────────────────────────────
LOG_PATH = "logs/system_log.txt"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("🛡️ QuantumShield Initialisierung...")

# ─── Matrix & Herzverbindung starten ───────────────────────────────────────
starte_kristallverbindung()
herzmodul = HerzKontrollModul()
herzmodul.aktiviere()
herzmodul.sende_signal("LEX-Kommunikation")
herzmodul.sende_signal("Nachrichtensystem")

# ─── Sprach-Engine ─────────────────────────────────────────────────────────
def aurora_spricht(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    logging.info(f"🔊 AURORA sagt: {text}")
    engine.say(text)
    engine.runAndWait()

# ─── Spracherkennung ───────────────────────────────────────────────────────
def spracherkennung():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        aurora_spricht("Bitte sprich jetzt.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language="de-DE")
            print(f"🧠 Erkannt: {text}")
            return text
        except sr.UnknownValueError:
            aurora_spricht("Sprache nicht erkannt.")
        except sr.RequestError as e:
            aurora_spricht(f"Fehler beim Spracherkennungsdienst: {e}")
        return None

# ─── FastAPI App ───────────────────────────────────────────────────────────
app = FastAPI(title="QuantumShield 3.0 – KI-Schutzinstanz")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = "user_api.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS benutzer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    benutzername TEXT UNIQUE NOT NULL,
    passwort_hash TEXT NOT NULL,
    rolle TEXT DEFAULT 'user',
    token TEXT,
    token_ablauf DATETIME
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS nachrichten (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inhalt TEXT NOT NULL
)""")
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

# ─── Schutzprüfung ─────────────────────────────────────────────────────────
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

# ─── Routen: Benutzer & Authentifizierung ──────────────────────────────────
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

# ─── Routen: Nachrichten / Sprachnachrichten ───────────────────────────────
@app.post("/senden")
def nachricht_senden(nachricht: Nachricht, token: str = Header(None)):
    pruefe_token_rolle(token)
    cursor.execute("INSERT INTO nachrichten (inhalt) VALUES (?)", (nachricht.inhalt,))
    conn.commit()
    return {"antwort": f"Nachricht gespeichert: '{nachricht.inhalt}'"}

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
        return {"antwort": "Keine Nachricht erkannt."}

@app.get("/nachrichten")
def nachrichten_abrufen(token: str = Header(None)):
    pruefe_token_rolle(token)
    cursor.execute("SELECT inhalt FROM nachrichten")
    daten = cursor.fetchall()
    return {"gespeichert": [eintrag[0] for eintrag in daten]}

# ─── Systemstatus & Bedrohungsscan ─────────────────────────────────────────
startzeitpunkt = time.time()

@app.get("/status_system")
def system_status():
    laufzeit = round(time.time() - startzeitpunkt, 2)
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    status_text = f"Laufzeit: {laufzeit}s – CPU: {cpu}% – RAM: {ram}%"
    aurora_spricht(status_text)
    if cpu > 85 or ram > 85:
        herzmodul.sende_signal("WARNUNG: Hohe Auslastung")
    return {"status": status_text}

@app.get("/shadowbyte_scan")
def shadowbyte_scan():
    verdächtige_prozesse = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if "hacker" in proc.info['name'].lower() or "exploit" in proc.info['name'].lower():
                verdächtige_prozesse.append(proc.info)
        except:
            continue
    if verdächtige_prozesse:
        herzmodul.sende_signal("ALARM: ShadowByte-Erkennung")
        aurora_spricht("Achtung! Bedrohung erkannt.")
        return {"meldung": "Gefahr erkannt!", "prozesse": verdächtige_prozesse}
    return {"meldung": "System sauber."}

# ─── WebSocket-Einstiegspunkt für LEX / Terminal ───────────────────────────
@app.websocket("/ws/core")
async def websocket_core(websocket: WebSocket):
    await websocket.accept()
    aurora_spricht("WebSocket-Verbindung aktiv.")
    try:
        while True:
            data = await websocket.receive_text()
            aurora_spricht(f"Empfangen: {data}")
            await websocket.send_text(f"Empfang bestätigt: {data}")
    except WebSocketDisconnect:
        aurora_spricht("WebSocket getrennt.")

# ─── GUI optional bereitstellen ────────────────────────────────────────────
if os.path.isdir("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
else:
    print("⚠️ Kein GUI-Ordner gefunden – statische Oberfläche nicht aktiv.")
