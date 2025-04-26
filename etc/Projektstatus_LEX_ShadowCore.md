# 🌌 QuantumShield Projektstatus – LEX & ShadowCore

## 🧠 Architekturüberblick

Du entwickelst eine vollständig offlinefähige, sprachgesteuerte KI-Kontrolleinheit, bestehend aus:

- **LEX (Windows / VS Code)**
  - Sprachbefehlserkennung via Mikrofon (speech_recognition)
  - Ausgabe via TTS (pyttsx3)
  - Steuerung per Zahlen oder Sprache
  - Socket-Verbindung zu ShadowCore
  - GUI-Integration (geplant)

- **ShadowCore (Kali Linux)**
  - Empfängt Befehle über Socket (Port 19840)
  - Führt Shell-Befehle aus (`/bin/bash`)
  - Gibt direkte Rückmeldung ins Terminal
  - Logging-Modul: `/root/shadowcore_befehle.log`
  - Systemd-Service für Autostart (funktioniert)

---

## ✅ Aktueller Funktionsstand

| Komponente | Status |
|------------|--------|
| 🔌 Socketverbindung | Erfolgreich verbunden 127.0.0.1 → ShadowCore |
| 🎙️ Spracheingabe | Aktiv, robust (LEX) |
| 🔊 TTS Feedback | Funktionsfähig |
| 🛡️ shadowcore_receiver.py | Läuft, führt Kommandos korrekt aus |
| 📜 Logging (shadowcore_logger.py) | Integriert, schreibt Zeit+Befehl |
| 🪪 systemd-Autostart (shadowcore.service) | Aktiviert, funktioniert |
| 🔎 Fehlerbehandlung bei leeren/falschen Befehlen | Implementiert |
| ⚠️ Probleme mit mehrfachen Socket-Binds | Erkannt & gelöst über Port-Freigabe |
| ❌ Fehler: Port 19840 schon belegt | → Prozesssuche & manuelle Freigabe durchgeführt |
| 🧱 Dateisystemsteuerung | Noch nicht aktiv |
| 🌐 GUI-Dashboard | Noch nicht integriert |

---

## 🔧 Struktur & Pfade

**Windows (LEX):**
- `lex_supervisor_socketlink.py` → Socket-Sender mit Sprachlogik
- `lex_supervisor_menu.py` → TTS-Menüführung
- `C:\Users\denni\OneDrive\Dokumente\Venv\QuantumShield 3.0\`

**Kali Linux (ShadowCore):**
- `/root/shadowcore_receiver.py` → Socket-Server
- `/root/shadowcore_logger.py` → Log-Funktion
- `/root/shadowcore_befehle.log` → Ausgabeprotokoll
- `/etc/systemd/system/shadowcore.service` → systemd-Integration

---

## 🧭 Nächste Entwicklungsstufen

| Ziel | Beschreibung |
|------|--------------|
| 🗂 Sprachgesteuerte Dateisuche | „Finde Datei .pdf“, „Öffne Downloads“ |
| 🔒 Passwortschutz für kritische Befehle | Sicherheitslayer für `shutdown`, `rm`, `apt upgrade` |
| 📡 LEX → ShadowCore mit Rückkanal | Antwort per Sprache / Bildschirm |
| 📊 Live-Visualisierung (Shield-Dashboard) | GUI oder Webansicht mit Aktivitätsübersicht |
| 🧠 Adaptive Befehlsgewichtung | LEX erkennt Muster und priorisiert selbst |
| 📤 Log Export (CSV/JSON) | Alle Logs exportierbar zur Analyse |

---

## ⚠️ Wichtig erkannte Hindernisse (gelöst)

- ❌ Port 19840 war belegt → systemctl shadowcore + eigener manueller Start → Konflikt  
  ✅ Lösung: nur **eine Instanz aktiv** (systemd ODER manuell mit Python)

- ❌ shadowcore_logger.py fehlte / war nicht auffindbar  
  ✅ Datei übertragen & eingebunden → Logging erfolgreich

- ❌ Autostart service meldete `Unit not found`  
  ✅ shadowcore.service korrekt in `/etc/systemd/system/` installiert, `daemon-reexec` ausgeführt

---

## 💾 Speichervorschlag

📝 **Speichern als:**
```bash
C:\Users\denni\OneDrive\Dokumente\Venv\QuantumShield 3.0\Projektstatus_LEX_ShadowCore.md
