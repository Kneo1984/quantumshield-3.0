# verschluessle_mit_stegano_reworked.py

import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from stegano import lsb
import secrets
from getpass import getpass

def generate_key(password: bytes, salt: bytes) -> bytes:
    """Schlüsselerzeugung auf Militärniveau mit PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,  # AES-256 braucht 32 Bytes
        salt=salt,
        iterations=500000,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_message(message: str, password: str) -> bytes:
    """Nachricht AES-256 verschlüsseln."""
    salt = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    key = generate_key(password.encode(), salt)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(message.encode()) + encryptor.finalize()

    return base64.urlsafe_b64encode(salt + iv + encrypted)

def hide_message_in_image(image_path: str, secret_message: str, password: str):
    """Versteckt die verschlüsselte Nachricht im Bild."""
    print("🔒 Starte Hochsicherheitsverschlüsselung...")
    encrypted_message = encrypt_message(secret_message, password)

    new_image_path = image_path.replace(".png", "_VERSTECKT.png")
    lsb.hide(image_path, encrypted_message.decode()).save(new_image_path)

    print(f"✅ Erfolgreich gespeichert als: {new_image_path}")

if __name__ == "__main__":
    image_path = input("📂 Pfad zum Bild: ").strip()
    secret_message = input("🧠 Geheime Nachricht: ").strip()

    print("\n🔑 Bitte starkes Passwort eingeben (mind. 20 Zeichen, Sonderzeichen empfohlen):")
    password = getpass()

    if len(password) < 20:
        print("❗ Passwort zu kurz! Sicherheit nicht gewährleistet. Vorgang abgebrochen.")
        exit(1)

    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
        print("❗ Passwort enthält keine Sonderzeichen! Sicherheit nicht gewährleistet. Vorgang abgebrochen.")
        exit(1)

    hide_message_in_image(image_path, secret_message, password)
