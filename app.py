import os
import logging
import requests
import gspread
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials

# ---------------- Logging ----------------
logging.basicConfig(level=logging.INFO)

# ---------------- Flask App ----------------
app = Flask(__name__)

# ---------------- Telegram Token ----------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8100473808:AAEF00mdUg5wKClRA8D_Nm03aES5iBQYsQ4")
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# ---------------- Google Sheets Setup ----------------
SHEET_ID = os.getenv("SHEET_ID", "1V3mBt5BkXRSjLLDHJoN1bfO35mgs56whdCGGHpC6DNM")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# ---------------- Telegram Webhook Endpoint ----------------
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Write to Google Sheet
        sheet.append_row([text])

        # Reply back
        send_message(chat_id, f"तुझा मेसेज Sheet मध्ये सेव्ह केला आहे: {text}")
    return "OK"

# ---------------- Send Message Function ----------------
def send_message(chat_id, text):
    url = f"{TELEGRAM_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# ---------------- Home Page ----------------
@app.route("/", methods=["GET"])
def home():
    return "Bot चालू आहे ✅"

# ---------------- Main ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
