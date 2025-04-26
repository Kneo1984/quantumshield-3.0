# quantumshield_ip_protector.py

import socket
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from stegano import lsb
from getpass import getpass
import secrets
import datetime
import os

def get_local_ip():
    """Lokale IP-Adresse automatisch holen."""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def generate_key(password: bytes, salt: bytes) -> bytes:
    """Schlüssel generieren."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=500000,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_message(message: str, password: str) -> bytes:
    """IP verschlüsseln."""
    salt = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    key = generate_key(password.encode(), salt)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(message.encode()) + encryptor.finalize()

    return base64.urlsafe_b64encode(salt + iv + encrypted)

def hide_message_in_image(image_path: str, encrypted_message: bytes):
    """Verstecke verschlüsselte IP im Bild."""
    new_image_path = image_path.replace(".png", "_IP_SAVED.png")
    lsb.hide(image_path, encrypted_message.decode()).save(new_image_path)
    return new_image_path

def save_log(log_message: str):
    """Protokolliere den Vorgang."""
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"{logs_dir}/quantumshield_log_{now}.txt", "w") as f:
        f.write(log_message)

if __name__ == "__main__":
    print("🔍 Lokale IP wird gesichert...")
    ip = get_local_ip()
    print(f"📍 Lokale IP-Adresse erkannt: {ip}")

    print("\n🔑 Passwort für Schutz eingeben (mind. 20 Zeichen, Sonderzeichen empfohlen):")
    password = getpass()

    if len(password) < 20:
        print("❗ Passwort zu schwach. Vorgang abgebrochen.")
        exit(1)

    if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password):
        print("❗ Passwort ohne Sonderzeichen. Vorgang abgebrochen.")
        exit(1)

    encrypted_ip = encrypt_message(ip, password)

    image_path = input("\n📂 Pfad zum Basis-Bild eingeben (PNG): ").strip()

    try:
        output_image = hide_message_in_image(image_path, encrypted_ip)
        print(f"✅ IP erfolgreich versteckt in: {output_image}")

        save_log(f"{datetime.datetime.now()}\nLokale IP {ip} verschlüsselt und versteckt.")
        print(f"✅ Log gespeichert.")
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")
        exit(1)
