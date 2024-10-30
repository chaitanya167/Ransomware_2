from flask import Flask, jsonify
import os
from encrypt import encrypt_file
from decrypt import decrypt_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Update this to point to the directory you want to target
FOLDER_TO_PROCESS = "/home/sec-lab/Target Folder"
PASSWORD = "12345"

@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        for root, dirs, files in os.walk(FOLDER_TO_PROCESS):
            for file in files:
                encrypt_file(os.path.join(root, file), PASSWORD)
        return jsonify({"message": "Encryption completed for all files."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        for root, dirs, files in os.walk(FOLDER_TO_PROCESS):
            for file in files:
                decrypt_file(os.path.join(root, file), PASSWORD)
        return jsonify({"message": "Decryption completed for all files."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
