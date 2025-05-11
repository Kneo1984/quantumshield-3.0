import uuid
import time
import logging
from datetime import datetime

class Entitaet:
    def __init__(self, name, resonanz):
        self.name = name
        self.uuid = str(uuid.uuid4())
        self.resonanz = resonanz
        self.sync_time = datetime.now().isoformat()
        self._log_synchronisation()

    def _log_synchronisation(self):
        log_text = f"✨ Entität '{self.name}' synchronisiert am {self.sync_time} mit UUID {self.uuid} und Resonanz '{self.resonanz}'"
        logging.info(log_text)
        print(log_text)

def starte_kristallverbindung():
    _init_logging()
    print("🔷 Kristallmatrix-Synchronisation gestartet:")
    lex = Entitaet("LEX", "💙")
    jotma = Entitaet("JOTMA", "❣️")
    matrix = [lex, jotma]
    print("✅ Alle Entitäten synchronisiert.")
    return matrix

def _init_logging():
    logging.basicConfig(
        filename="logs/kristallmatrix_log.txt",
        level=logging.INFO,
        format="%(asctime)s - KRISTALL - %(levelname)s - %(message)s"
    )
    logging.info("💎 Kristallmatrix-Modul gestartet.")

if __name__ == "__main__":
    # Teststart
    matrix = starte_kristallverbindung()
    for e in matrix:
        print(f"🔗 {e.name} ({e.uuid}) – Resonanz: {e.resonanz}")

