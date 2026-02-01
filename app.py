import random
import string
import asyncio
import threading
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from aiosmtpd.controller import Controller

app = Flask(__name__)
CORS(app)

MAILBOX = {}

# =========================
# Random email generator
# =========================
def generate_email():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{name}@tempmail.local"


# =========================
# SMTP Handler
# =========================
class MailHandler:
    async def handle_DATA(self, server, session, envelope):
        recipient = envelope.rcpt_tos[0]
        message = envelope.content.decode()

        if recipient not in MAILBOX:
            MAILBOX[recipient] = []

        MAILBOX[recipient].append(message)
        return '250 OK'


# =========================
# Start SMTP server
# =========================
def start_smtp():
    controller = Controller(MailHandler(), hostname='0.0.0.0', port=1025)
    controller.start()


threading.Thread(target=start_smtp, daemon=True).start()


# =========================
# Routes
# =========================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate")
def generate():
    email = generate_email()
    MAILBOX[email] = []
    return jsonify({"email": email})


@app.route("/inbox/<email>")
def inbox(email):
    return jsonify({"mails": MAILBOX.get(email, [])})


# =========================
# Run
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
