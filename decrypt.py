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

def decrypt_file(file_path, password):
    try:
        with open(file_path, 'rb') as file:
            salt = file.read(16)  # Read the salt (first 16 bytes)
            iv = file.read(16)    # Read the IV (next 16 bytes)
            encrypted_data = file.read()

        key = derive_key(password.encode(), salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = PKCS7(128).unpadder()
        # Correct the reference to unpadded_data assignment here
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

        with open(file_path, 'wb') as dec_file:
            dec_file.write(unpadded_data)

        return f"File decrypted successfully: {file_path}"
    
    except Exception as e:
        return f"Error decrypting file {file_path}: {str(e)}"

if __name__ == "__main__":
    FOLDER_TO_PROCESS = "/home/sec-lab/Target Folder"
    for root, dirs, files in os.walk(FOLDER_TO_PROCESS):
        for file in files:
            decrypt_file(os.path.join(root, file), PASSWORD)
