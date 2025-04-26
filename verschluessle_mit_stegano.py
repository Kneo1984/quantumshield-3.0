from cryptosteganography import CryptoSteganography
from Crypto.Cipher import AES
import base64

# 🔐 Schritt 1: Geheime Nachricht
urspruengliche_nachricht = "REVOLUTION_START_2025"

# 🔐 Schritt 2: AES-256-Verschlüsselung
aes_passwort = "Aurora_Herzmatrix_256bit"
aes_key = aes_passwort.ljust(32)[:32].encode("utf-8")
cipher = AES.new(aes_key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(urspruengliche_nachricht.encode("utf-8"))

# 🧪 Kombiniere nonce + tag + ciphertext für spätere Entschlüsselung
kombiniert = base64.b64encode(cipher.nonce + tag + ciphertext).decode("utf-8")

# 🔄 Schritt 3: Caesar-Rotationsverschlüsselung (Shift 7)
def caesar(text, shift=7):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

rotated = caesar(kombiniert, shift=7)

# 🖼️ Schritt 4: Steganografie ins Bild
steg = CryptoSteganography(aes_passwort)
bildquelle = "C:/Users/denni/OneDrive/Bilder/Selbstgemachte_Bilder_KI/Mount_Everest_Me3.jpg.png"
bild_ziel = "C:/Users/denni/OneDrive/Bilder/Selbstgemachte_Bilder_KI/Mount_Everest_Me3_VERSTECKT.png"

steg.hide(bildquelle, bild_ziel, rotated)
print(f"✅ Verschlüsselung erfolgreich. Gespeichert als: {bild_ziel}")
