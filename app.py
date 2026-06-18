from flask import Flask, render_template, request, session, redirect
import sqlite3
import webbrowser
import threading
import logging
import html
import re

from functools import wraps

from config import DATABASE
from database import init_db

from ml_pipeline.predictor import predict_email
from detection.url_analyzer import extract_domains
from detection.dns_checker import dns_check
from detection.brand_detector import brand_mismatch
from detection.keyword_engine import keyword_score
from detection.sender_checker import verify_sender

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"

init_db()

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

logging.basicConfig(
    filename="scanner.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect("/")
        return f(*args, **kwargs)
    return wrapper


def analyze(email_text, sender):

    alerts = []

    risk, _ = predict_email(email_text)

    domains = extract_domains(email_text)

    if domains:
        for d in domains:
            if not dns_check(d):
                alerts.append(f"Domain does not resolve: {d}")
                risk += 20
    else:
        alerts.append("No URLs detected")

    brand_alerts = brand_mismatch(email_text, domains)
    alerts.extend(brand_alerts)

    if brand_alerts:
        risk += 20

    kscore, khits = keyword_score(email_text)
    risk += kscore
    alerts.extend(khits)

    sender_score, sender_alerts = verify_sender(sender, email_text)
    risk += sender_score
    alerts.extend(sender_alerts)

    risk = min(risk, 100)

    if risk >= 80:
        result = "PHISHING 🚨"
    elif risk >= 50:
        result = "SUSPICIOUS ⚠️"
    else:
        result = "SAFE ✅"

    logging.info(
        f"Sender={sender} Risk={risk} Result={result}"
    )

    return risk, result, alerts


@app.route("/", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def home():

    outputs = []

    if request.method == "POST":

        senders = request.form.getlist("sender[]")
        emails = request.form.getlist("email[]")

        for sender, email_text in zip(senders, emails):

            sender = html.escape(sender.strip())
            email_text = html.escape(email_text.strip())

            if not sender or not email_text:
                continue

            if not EMAIL_REGEX.match(sender):
                outputs.append({
                    "sender": sender,
                    "email": "",
                    "risk": 100,
                    "result": "INVALID EMAIL",
                    "alerts": ["Invalid sender format"]
                })
                continue

            risk, result, alerts = analyze(email_text, sender)

            conn = sqlite3.connect(DATABASE)

            conn.execute(
                "INSERT INTO logs(risk,result,email) VALUES(?,?,?)",
                (risk, result, email_text[:500])
            )

            conn.commit()
            conn.close()

            outputs.append({
                "sender": sender,
                "email": email_text[:120],
                "risk": risk,
                "result": result,
                "alerts": alerts
            })

    return render_template(
        "index.html",
        outputs=outputs
    )


@app.route("/admin")
@login_required
def admin():

    conn = sqlite3.connect(DATABASE)

    rows = conn.execute(
        "SELECT * FROM logs ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        rows=rows
    )


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )