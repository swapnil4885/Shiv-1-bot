import os
from flask import Flask, request
import requests
import openai

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route("/health")
def health():
    return "OK", 200

@app.route("/update", methods=["POST", "GET"])
def update():
    try:
        prompt = "Give today's Nifty scalping radar update in brief."
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        message = completion.choices[0].message["content"]
        send_telegram_message(f"📊 *Shiv Pro Scalping Radar*\n\n{message}")
        return "Sent", 200
    except Exception as e:
        return str(e), 500

@app.route("/cron/morning")
def cron_morning():
    send_telegram_message("🌅 Good Morning! Market Radar is live for today.")
    return "Morning update sent", 200

@app.route("/cron/evening")
def cron_evening():
    send_telegram_message("🌇 Market closed. Evening summary coming soon.")
    return "Evening update sent", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
