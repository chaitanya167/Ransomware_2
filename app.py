import logging
from flask import Flask, jsonify
import os
from encrypt import encrypt_file
from decrypt import decrypt_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

FOLDER_TO_PROCESS = "/home/sec-lab/Target Folder"
PASSWORD = "12345"

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        for root, _, files in os.walk(FOLDER_TO_PROCESS):
            for file in files:
                file_path = os.path.join(root, file)
                result = encrypt_file(file_path, PASSWORD)
                logging.info(f"Encrypted {file_path}: {result}")
        return jsonify({"message": "Encryption completed for all files."}), 200
    except Exception as e:
        logging.error(f"Error during encryption: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        for root, _, files in os.walk(FOLDER_TO_PROCESS):
            for file in files:
                file_path = os.path.join(root, file)
                result = decrypt_file(file_path, PASSWORD)
                logging.info(f"Decrypted {file_path}: {result}")
        return jsonify({"message": "Decryption completed for all files."}), 200
    except Exception as e:
        logging.error(f"Error during decryption: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
