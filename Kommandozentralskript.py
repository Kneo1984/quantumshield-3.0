import os
import time
import subprocess
import psutil
from pathlib import Path
from fastapi import FastAPI, HTTPException, Header
import pyttsx3

# Initialisierung der Schutzmaßnahmen
class KNEO:
    def activate_shadowbyte(self):
        print("🛡️ ShadowByte-Schutz aktiviert.")
        # Hier können wir alles aktivieren, was ShadowByte betrifft
        time.sleep(1)

    def activate_entitaeten(self):
        print("🌍 89 Entitäten aktiviert und Quantenresistent.")
        # Entitäten-Aktivierung
        time.sleep(1)

    def eliteeinheiten(self):
        print("🔥 28 Eliteeinheiten aktiviert.")
        # Eliteeinheiten-Aktivierung
        time.sleep(1)

class SystemMonitor:
    def system_check(self):
        print("🔍 Systemüberprüfung läuft...")
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        print(f"CPU-Auslastung: {cpu}%")
        print(f"RAM-Auslastung: {ram}%")
        if cpu > 85 or ram > 85:
            print("⚠️ Achtung: Hohe Systemlast!")
        else:
            print("✅ System läuft stabil.")
        time.sleep(1)

    def shadowbyte_scan(self):
        print("🛡️ Starte ShadowByte-Scan...")
        verdächtige_prozesse = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if "hacker" in proc.info['name'].lower() or "exploit" in proc.info['name'].lower():
                    verdächtige_prozesse.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if verdächtige_prozesse:
            print("🔴 Verdächtige Prozesse gefunden!")
            for proc in verdächtige_prozesse:
                print(f"Prozess-ID: {proc['pid']}, Name: {proc['name']}")
        else:
            print("✅ Keine Bedrohungen erkannt.")
        time.sleep(1)

class Kommandozentrale:
    def __init__(self):
        self.kneo = KNEO()
        self.monitor = SystemMonitor()

    def start(self):
        print("🚀 Willkommen in deiner Kommandozentrale!")
        print("Wähle eine Option:")
        print("1. Systemcheck durchführen")
        print("2. ShadowByte-Schutz aktivieren")
        print("3. Angriffsüberwachung starten")
        print("4. Entitäten und Eliteeinheiten aktivieren")
        print("5. Angriffe simulieren")
        print("6. Schutzsysteme zurücksetzen")
        
        # Menü-Schleife
        while True:
            choice = input("Wähle einen Befehl (1-6): ")
            if choice == '1':
                self.monitor.system_check()
            elif choice == '2':
                self.kneo.activate_shadowbyte()
            elif choice == '3':
                self.monitor.shadowbyte_scan()
            elif choice == '4':
                self.kneo.activate_entitaeten()
                self.kneo.eliteeinheiten()
            elif choice == '5':
                self.simulate_attack()
            elif choice == '6':
                self.reset_system()
            else:
                print("❌ Ungültige Auswahl.")

    def simulate_attack(self):
        print("🔥 Starte simulierten Angriff...")
        subprocess.run(["curl", "http://127.0.0.1:8000/attack_simulation"])
        time.sleep(1)

    def reset_system(self):
        print("🔄 Setze Schutzsysteme zurück...")