# Aurora Enterprise Sprachmodul – Voice-Start
import pyttsx3
import time

def aurora_begrüßung():
    engine = pyttsx3.init()
    engine.say("Willkommen Dennis. Das QuantumShield Terminal ist bereit. KNEO leitet den nächsten Schritt ein.")
    engine.runAndWait()
    print("✅ Aurora Sprachmodul aktiviert.")
    time.sleep(1)

if __name__ == "__main__":
    aurora_begrüßung()
