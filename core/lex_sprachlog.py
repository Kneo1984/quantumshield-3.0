# lex_sprachlog.py
# 📋 Modul: Sprachlog – QuantumShield System
# Funktion: Speichert letzte Sprachbefehle lokal

import datetime

log_datei = "sprachlog.txt"

# 🌟 Funktion zum Eintrag speichern
def speichere_sprachbefehl(befehl):
    zeitstempel = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    eintrag = f"[{zeitstempel}] {befehl}\n"
    with open(log_datei, "a", encoding="utf-8") as datei:
        datei.write(eintrag)

# 🌟 Funktion zum letzten Befehl anzeigen
def letzter_befehl():
    try:
        with open(log_datei, "r", encoding="utf-8") as datei:
            zeilen = datei.readlines()
            if zeilen:
                print(f"🧠 Letzter Befehl: {zeilen[-1].strip()}")
            else:
                print("⚠️ Keine Einträge vorhanden.")
    except FileNotFoundError:
        print("⚠️ Sprachlogdatei nicht gefunden.")
