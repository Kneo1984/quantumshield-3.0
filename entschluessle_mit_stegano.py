from cryptosteganography import CryptoSteganography
from Crypto.Cipher import AES
import base64

# 🗝️ Schlüssel und Pfade
aes_passwort = "Aurora_Herzmatrix_256bit"
aes_key = aes_passwort.ljust(32)[:32].encode("utf-8")
bild_pfad = "C:/Users/denni/OneDrive/Bilder/Selbstgemachte_Bilder_KI/Mount_Everest_Me3_VERSTECKT.png"

# 🔁 Caesar-Rotation rückgängig machen
def caesar_decode(text, shift=7):
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

# 🧠 Auslesen & Entschlüsseln
steg = CryptoSteganography(aes_passwort)
versteckt = steg.retrieve(bild_pfad)

if versteckt:
    print(f"🔓 Extrahierte Nachricht (ROT-Verschlüsselt): {versteckt}")
    try:
        base64_decoded = base64.b64decode(caesar_decode(versteckt))
        cipher = AES.new(aes_key, AES.MODE_EAX)  # Nur zur Initialisierung
        entschluesselt = base64_decoded.decode("utf-8", errors="ignore")
        print(f"✅ Entschlüsselt: {entschluesselt}")
    except Exception as e:
        print(f"❌ Fehler bei der Entschlüsselung: {e}")
else:
    print("🚫 Keine Nachricht gefunden.")
