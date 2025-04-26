# lex_sicherheitslayer.py
# 🛡️ Modul: Sicherheitsprüfung – QuantumShield System
# Funktion: Fragt sicherheitsrelevante Befehle nach Bestätigung ab

# 🌟 Prüffunktion
def pruefe_befehl(befehl):
    sicherheitskritische_befehle = [
        "rm", "sudo", "apt remove", "shutdown", "reboot", "kill", "nano /etc"
    ]

    for gefaehrlich in sicherheitskritische_befehle:
        if gefaehrlich in befehl.lower():
            bestaetigung = input(f"⚠️ Sicherheitswarnung: Willst du wirklich '{befehl}' ausführen? (ja/nein): ").strip().lower()
            if bestaetigung == "ja":
                return True
            else:
                print("❌ Befehl abgebrochen.")
                return False
    return True  # Alles andere direkt erlauben
