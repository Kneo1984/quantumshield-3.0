# lex_dateisuche.py
# 📂 Modul: Sprachgesteuerte Dateisuche – QuantumShield System
# Funktion: Findet Dateien nach Sprachbefehl
# Sicher und beendbar

import os

# 🌟 Funktion zur Dateisuche
def suche_datei(startverzeichnis, suchbegriff):
    gefundene_dateien = []
    for ordnername, unterordner, dateien in os.walk(startverzeichnis):
        for datei in dateien:
            if suchbegriff.lower() in datei.lower():
                gefundene_dateien.append(os.path.join(ordnername, datei))
    return gefundene_dateien

# 🌟 Startfunktion
def starte_dateisuche():
    print("🔎 Starte Dateisuche...")
    suchbegriff = input("Bitte gib einen Dateinamen oder ein Stichwort ein: ")
    ergebnisse = suche_datei(os.path.expanduser("~"), suchbegriff)

    if ergebnisse:
        print(f"✅ {len(ergebnisse)} Datei(en) gefunden:")
        for datei in ergebnisse:
            print(f"- {datei}")
    else:
        print("❌ Keine Datei gefunden.")
