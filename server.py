from flask import Flask, request, jsonify, send_file
import json
import os
import socket
import qrcode

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'

# =========================
# AUTO DETECT IP
# =========================

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(("8.8.8.8", 80))

ip = s.getsockname()[0]

s.close()

url = f"http://{ip}:8000"

print()
print("===================================")
print("SCAN QR ATAU BUKA LINK INI:")
print(url)
print("===================================")
print()

# =========================
# GENERATE QR
# =========================

img = qrcode.make(url)

img.save("qr.png")

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/qr')
def qr():
    return send_file('qr.png')

@app.route('/send', methods=['POST'])
def send():

    text = request.form.get('text')

    file = request.files.get('file')

    if not os.path.exists('data.json'):

        with open('data.json', 'w') as f:
            json.dump([], f)

    with open('data.json', 'r') as f:
        messages = json.load(f)

    file_name = ""

    if file:

        file_name = file.filename

        file.save(os.path.join(UPLOAD_FOLDER, file_name))

    messages.append({
        'text': text,
        'file': file_name
    })

    with open('data.json', 'w') as f:
        json.dump(messages, f)

    return jsonify({
        'status': 'ok'
    })

@app.route('/get')
def get():

    try:
        with open('data.json', 'r') as f:
            data = json.load(f)

    except:
        data = []

    return jsonify(data)

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_file(
        os.path.join(UPLOAD_FOLDER, filename)
    )

app.run(host='0.0.0.0', port=8000)