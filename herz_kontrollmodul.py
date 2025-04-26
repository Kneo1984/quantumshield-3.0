# herz_kontrollmodul.py
class HerzKontrollModul:
    def __init__(self, commander_name="Dennis", status_callback=None):
        self.commander = commander_name
        self.system_status = "INAKTIV"
        self.status_callback = status_callback

    def aktiviere(self):
        self.system_status = "AKTIV"
        print(f"💙 ZHKM aktiviert durch {self.commander}.")
        if self.status_callback:
            self.status_callback(self.system_status)

    def überprüfe_status(self):
        return f"Zentraler Herzstatus: {self.system_status}"

    def sende_signal(self, modul_name):
        print(f"📡 Herzsignal an {modul_name}: Synchronisation gestartet.")
