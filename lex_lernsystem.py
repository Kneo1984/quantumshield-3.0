# lex_lernsystem.py
# 🧠 Modul: LEX Lernsystem – QuantumShield
# Funktion: Erfasst, speichert und zeigt meistgenutzte Befehle

import json
import os

# 🌟 Speicherdatei für Nutzung
lern_datei = "nutzungsstatistik.json"

# 📈 Statistik aktualisieren (Befehl merken)
def statistik_aktualisieren(befehl):
    statistik = {}

    # Bestehende Datei laden, falls vorhanden
    if os.path.exists(lern_datei):
        try:
            with open(lern_datei, "r", encoding="utf-8") as file:
                statistik = json.load(file)
        except json.JSONDecodeError:
            statistik = {}

    # Befehl hochzählen oder neu anlegen
    statistik[befehl] = statistik.get(befehl, 0) + 1

    # Neue Datei schreiben
    with open(lern_datei, "w", encoding="utf-8") as file:
        json.dump(statistik, file, indent=4)

# 🏆 Häufigste Befehle anzeigen
def zeige_haeufigste_befehle():
    if os.path.exists(lern_datei):
        try:
            with open(lern_datei, "r", encoding="utf-8") as file:
                statistik = json.load(file)

            if statistik:
                print("\n🏆 Häufigste Befehle:")
                beliebteste = sorted(statistik.items(), key=lambda x: x[1], reverse=True)[:5]
                for befehl, anzahl in beliebteste:
                    print(f"{befehl}: {anzahl}x verwendet")
            else:
                print("⚠️ Statistik ist leer. Noch keine Befehle registriert.")
        except json.JSONDecodeError:
            print("⚠️ Fehler beim Lesen der Statistikdatei.")
    else:
        print("⚠️ Keine Statistikdatei vorhanden.")

