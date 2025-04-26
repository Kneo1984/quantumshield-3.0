# /root/shadowcore_logger.py
# 📜 Logging-Modul für ShadowCore
from datetime import datetime
import shadowcore_logger
...
shadowcore_logger.logge_befehl(data)

def logge_befehl(befehl):
    zeit = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("/root/shadowcore_befehle.log", "a") as f:
        f.write(f"{zeit} {befehl}\n")
