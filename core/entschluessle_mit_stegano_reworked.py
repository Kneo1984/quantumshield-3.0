# entschluessle_mit_stegano_reworked.py

import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from stegano import lsb
from getpass import getpass

def generate_key(password: bytes, salt: bytes) -> bytes:
    """Erzeugt denselben AES-Schlüssel aus Passwort und Salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=500000,
        backend=default_backend()
    )
    return kdf.derive(password)

def decrypt_message(encrypted_data: bytes, password: str) -> str:
    """Entschlüsselt die Nachricht."""
    raw = base64.urlsafe_b64decode(encrypted_data)
    salt = raw[:16]
    iv = raw[16:32]
    encrypted = raw[32:]
    key = generate_key(password.encode(), salt)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()

    return decrypted.decode()

def reveal_message_from_image(image_path: str, password: str):
    """Extrahiert und entschlüsselt die versteckte Nachricht aus einem Bild."""
    print("🔎 Extrahiere versteckte Nachricht...")
    encrypted_message = lsb.reveal(image_path)

    if encrypted_message is None:
        print("❌ Keine versteckte Nachricht gefunden oder Bild wurde beschädigt!")
        exit(1)

    print("🔓 Entschlüssele Nachricht...")
    try:
        message = decrypt_message(encrypted_message.encode(), password)
        print(f"✅ Entschlüsselte Nachricht: {message}")
    except Exception as e:
        print("❌ Entschlüsselung fehlgeschlagen! Falsches Passwort oder Bild beschädigt.")
        exit(1)

if __name__ == "__main__":
    image_path = input("📂 Pfad zum Bild: ").strip()

    print("\n🔑 Passwort für Entschlüsselung eingeben:")
    password = getpass()

    reveal_message_from_image(image_path, password)
