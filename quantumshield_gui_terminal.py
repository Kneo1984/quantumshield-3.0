
import tkinter as tk
import subprocess
import threading

def ausgabe_anzeigen(text):
    ausgabe_feld.insert(tk.END, text + "\n")
    ausgabe_feld.see(tk.END)

def systemstatus_abrufen():
    try:
        result = subprocess.check_output(["curl", "http://127.0.0.1:8000/status_system"], text=True)
        ausgabe_anzeigen(result)
    except Exception as e:
        ausgabe_anzeigen(f"Fehler: {str(e)}")

def shadowbyte_scan():
    try:
        result = subprocess.check_output(["curl", "http://127.0.0.1:8000/shadowbyte_scan"], text=True)
        ausgabe_anzeigen(result)
    except Exception as e:
        ausgabe_anzeigen(f"Fehler: {str(e)}")

def sprache_senden():
    try:
        result = subprocess.check_output(["curl", "-X", "POST", "http://127.0.0.1:8000/nachricht_senden_mit_sprache"], text=True)
        ausgabe_anzeigen(result)
    except Exception as e:
        ausgabe_anzeigen(f"Fehler: {str(e)}")

def starten_threaded(funktion):
    threading.Thread(target=funktion).start()

fenster = tk.Tk()
fenster.title("QuantumShield™ Kommandozentrale")
fenster.geometry("700x450")
fenster.configure(bg="#0d1117")

titel = tk.Label(fenster, text="🔒 QuantumShield™ 3.0 – Kommandozentrale", bg="#0d1117", fg="cyan", font=("Consolas", 14))
titel.pack(pady=10)

btn1 = tk.Button(fenster, text="✅ Systemstatus prüfen", width=35, command=lambda: starten_threaded(systemstatus_abrufen))
btn1.pack(pady=5)

btn2 = tk.Button(fenster, text="🛡 ShadowByte-Scan starten", width=35, command=lambda: starten_threaded(shadowbyte_scan))
btn2.pack(pady=5)

btn3 = tk.Button(fenster, text="🎙 Sprach-Nachricht senden", width=35, command=lambda: starten_threaded(sprache_senden))
btn3.pack(pady=5)

ausgabe_feld = tk.Text(fenster, height=15, width=80, bg="#161b22", fg="lime", font=("Consolas", 10))
ausgabe_feld.pack(pady=10)

fenster.mainloop()
