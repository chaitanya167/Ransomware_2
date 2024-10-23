from flask import Flask, request, jsonify, render_template_string
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.padding import PKCS7

app = Flask(__name__)

# Define the target folder for encryption and decryption
FOLDER_TO_PROCESS = "/home/sec-lab/Target Folder"  # Adjust this to your actual target folder
PASSWORD = "12345"  # Predefined password for encryption and decryption

# Helper function to derive the encryption key
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password)

# Encryption function
def encrypt_file(file_path, key, salt):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Overwrite the file with encrypted data
        with open(file_path, 'wb') as enc_file:
            enc_file.write(salt + iv + encrypted_data)

        return f"File encrypted successfully: {file_path}"
    except Exception as e:
        return f"Error encrypting file {file_path}: {str(e)}"

# Decryption function
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
        unpadded_data = unpadder.update(decrypted_data) + unpadded_data.finalize()

        # Overwrite the encrypted file with the decrypted content
        with open(file_path, 'wb') as dec_file:
            dec_file.write(unpadded_data)

        return f"File decrypted successfully: {file_path}"
    except Exception as e:
        return f"Error decrypting file {file_path}: {str(e)}"

# Route for the home page
@app.route('/')
def home():
    return render_template_string('''
        <html>
            <head>
                <title>File Encryption & Decryption</title>
            </head>
            <body>
                <h1>Welcome to the File Encryption & Decryption App</h1>
                <p>Click below to encrypt or decrypt files in the target folder:</p>
                <form action="/encrypt" method="post">
                    <button type="submit">Encrypt Files</button>
                </form>
                <br>
                <form action="/decrypt" method="post">
                    <button type="submit">Decrypt Files</button>
                </form>
            </body>
        </html>
    ''')
# Route to handle encryption
@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        salt = os.urandom(16)
        key = derive_key(PASSWORD.encode(), salt)
        for root, _, files in os.walk(FOLDER_TO_PROCESS):
            for file in files:
                file_path = os.path.join(root, file)
                result = encrypt_file(file_path, key, salt)
                print(result)

        return jsonify({"message": "Encryption completed for all files."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle decryption
@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        for root, _, files in os.walk(FOLDER_TO_PROCESS):
            for file in files:
                file_path = os.path.join(root, file)
                result = decrypt_file(file_path, PASSWORD)
                print(result)

        return jsonify({"message": "Decryption completed for all files."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
