import random
import string
import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MAILBOX = {}


def generate_email():
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{name}@tempmail.local"


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


# optional: test route to simulate mail
@app.route("/demo/<email>/<msg>")
def demo(email, msg):
    MAILBOX.setdefault(email, []).append(msg)
    return {"ok": True}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )
