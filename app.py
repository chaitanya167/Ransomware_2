from flask import Flask, jsonify
import os
from encrypt import encrypt_file
from decrypt import decrypt_file

app = Flask(__name__)

# Define the target folder on your VM or in the Azure environment
TARGET_FOLDER = "/home/sec-lab/Target Folder"  # Update this path
PASSWORD = "12345"  # Set the password for encryption/decryption

@app.route('/')
def index():
    return jsonify(message="Welcome to the Encryption/Decryption App!")

@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Encrypt all files in the target folder
    for root, dirs, files in os.walk(TARGET_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            if encrypt_file(file_path, PASSWORD):
                print(f"File encrypted: {file_path}")
            else:
                return jsonify({"error": f"File encryption failed for {file_path}"}), 500
    return jsonify({"message": "All files encrypted successfully!"})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    # Decrypt all files in the target folder
    for root, dirs, files in os.walk(TARGET_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            if decrypt_file(file_path, PASSWORD):
                print(f"File decrypted: {file_path}")
            else:
                return jsonify({"error": f"File decryption failed for {file_path}"}), 500
    return jsonify({"message": "All files decrypted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

